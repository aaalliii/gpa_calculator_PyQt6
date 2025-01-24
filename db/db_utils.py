import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="gpa_db",
        user="postgres",
        password="sake",
        host="localhost",
        port="5432"
    )
    return conn

def check_remembered_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT uid FROM users WHERE isRemembered = TRUE LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def get_user_by_id(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT uid, name, username, pfp, theme, isRemembered FROM users WHERE uid=%s", (uid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            'uid': row[0],
            'name': row[1],
            'username': row[2],
            'pfp': row[3],
            'theme': row[4],
            'isRemembered': row[5]
        }
    return None

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT uid, name, username, pfp, theme, isRemembered FROM users WHERE username=%s AND password=%s",
                (username, password))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            'uid': row[0],
            'name': row[1],
            'username': row[2],
            'pfp': row[3],
            'theme': row[4],
            'isRemembered': row[5]
        }
    return None

def set_is_remembered(uid, val):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET isRemembered=%s WHERE uid=%s", (val, uid))
    conn.commit()
    cur.close()
    conn.close()

def register_user(name, username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, username, password)
            VALUES (%s, %s, %s)
        """, (name, username, password))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def fetch_sections(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT did, name, gpa FROM data WHERE uid=%s", (uid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {'did': r[0], 'name': r[1], 'gpa': r[2]}
        for r in rows
    ]

def create_section(uid, name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO data (uid, name) VALUES (%s, %s) RETURNING did", (uid, name))
    did = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return did

def rename_section(did, new_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE data SET name=%s WHERE did=%s", (new_name, did))
    conn.commit()
    cur.close()
    conn.close()

def delete_section(did):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM data WHERE did=%s", (did,))
    conn.commit()
    cur.close()
    conn.close()

def fetch_data_low(did):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT didl, courseName, grade, credits FROM datalow WHERE did=%s", (did,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {'didl': r[0], 'courseName': r[1], 'grade': r[2], 'credits': r[3]}
        for r in rows
    ]

def add_data_low(did, courseName, grade, credits):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO datalow (did, courseName, grade, credits)
        VALUES (%s, %s, %s, %s)
    """, (did, courseName, grade, credits))
    conn.commit()
    cur.close()
    conn.close()

def remove_data_low(didl):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM datalow WHERE didl=%s", (didl,))
    conn.commit()
    cur.close()
    conn.close()

def recalc_section_gpa(did):
    # Simple GPA calculation: sum of (grade * credits) / sum(credits)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT grade, credits FROM datalow WHERE did=%s", (did,))
    rows = cur.fetchall()

    if not rows:
        section_gpa = 0
    else:
        total_points = 0
        total_credits = 0
        for (grade, cr) in rows:
            total_points += (grade * cr)
            total_credits += cr
        section_gpa = total_points / total_credits if total_credits else 0

    # Update data table
    cur.execute("UPDATE data SET gpa=%s WHERE did=%s", (section_gpa, did))
    conn.commit()
    cur.close()
    conn.close()

def update_user_info(uid, name, pfp, theme):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET name=%s, pfp=%s, theme=%s
        WHERE uid=%s
    """, (name, pfp, theme, uid))
    conn.commit()
    cur.close()
    conn.close()
