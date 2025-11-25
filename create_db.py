import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "rms.db")

def create_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Create course & student tables (if not exists)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)
    con.commit()

    # Keep student table similar to before (we will use enrollment for courses)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,    -- legacy column; may be migrated to enrollment
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)
    con.commit()

    # Create result table with subject column (if not exists)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            subject TEXT,
            marks_ob INTEGER,
            full_marks INTEGER,
            per REAL
        )
    """)
    con.commit()

    # Create enrollment table to map students -> courses (many-to-many)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollment(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll INTEGER,
            cid INTEGER,
            UNIQUE(roll, cid)
        )
    """)
    con.commit()

    # Migration: if student.course has data, try to map to course.cid and insert into enrollment
    try:
        cur.execute("PRAGMA table_info(student)")
        cols = [r[1] for r in cur.fetchall()]
        if "course" in cols:
            # find students with non-empty course
            cur.execute("SELECT roll, course FROM student WHERE course IS NOT NULL AND TRIM(course) <> ''")
            rows = cur.fetchall()
            for roll, course_name in rows:
                # attempt to find course id
                cur.execute("SELECT cid FROM course WHERE name=?", (course_name,))
                res = cur.fetchone()
                if res:
                    cid = res[0]
                else:
                    # if course not exists, create it (so migration doesn't lose data)
                    cur.execute("INSERT OR IGNORE INTO course (name, duration, charges, description) VALUES (?, '', '', '')", (course_name,))
                    con.commit()
                    cur.execute("SELECT cid FROM course WHERE name=?", (course_name,))
                    cid = cur.fetchone()[0]
                # insert into enrollment (ignore duplicates)
                try:
                    cur.execute("INSERT OR IGNORE INTO enrollment (roll, cid) VALUES (?, ?)", (roll, cid))
                    con.commit()
                except Exception:
                    pass
    except Exception as e:
        print("Migration warning:", e)

    con.close()

if __name__ == "__main__":
    create_db()
    print("Database created/updated at:", DB_PATH)
