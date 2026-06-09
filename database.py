import sqlite3


# ---------------- DATABASE SETUP ---------------- #

def create_database():

    conn = sqlite3.connect(
        "interview_history.db"
    )

    cursor = conn.cursor()

    # Users Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Interviews Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        ats_score REAL,
        semantic_score REAL,
        interview_score REAL,
        hiring_decision TEXT,
        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# ---------------- USER FUNCTIONS ---------------- #

def register_user(
    name,
    email,
    password
):

    conn = sqlite3.connect(
        "interview_history.db"
    )

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users(
            name,
            email,
            password
        )
        VALUES(?,?,?)
        """, (
            name,
            email,
            password
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(
    email,
    password
):

    conn = sqlite3.connect(
        "interview_history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email=?
    AND password=?
    """, (
        email,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ---------------- INTERVIEW FUNCTIONS ---------------- #

def save_interview(
    user_id,
    date,
    ats_score,
    semantic_score,
    interview_score,
    hiring_decision
):

    conn = sqlite3.connect(
        "interview_history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO interviews(
        user_id,
        date,
        ats_score,
        semantic_score,
        interview_score,
        hiring_decision
    )
    VALUES(?,?,?,?,?,?)
    """, (
        user_id,
        date,
        ats_score,
        semantic_score,
        interview_score,
        hiring_decision
    ))

    conn.commit()
    conn.close()


# ---------------- HISTORY FUNCTIONS ---------------- #

def get_user_history(
    user_id
):

    conn = sqlite3.connect(
        "interview_history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        date,
        ats_score,
        semantic_score,
        interview_score,
        hiring_decision
    FROM interviews
    WHERE user_id=?
    ORDER BY id DESC
    """, (
        user_id,
    ))

    data = cursor.fetchall()

    conn.close()

    return data


# ---------------- USER INFO ---------------- #

def get_user_by_id(
    user_id
):

    conn = sqlite3.connect(
        "interview_history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE id=?
    """, (
        user_id,
    ))

    user = cursor.fetchone()

    conn.close()

    return user