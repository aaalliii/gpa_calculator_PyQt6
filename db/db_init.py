import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname="gpa_db",
        user="postgres",
        password="sake",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
      UID SERIAL PRIMARY KEY,
      name VARCHAR(100),
      username VARCHAR(100) UNIQUE NOT NULL,
      password VARCHAR(100) NOT NULL,
      pfp VARCHAR(255),
      theme VARCHAR(20) DEFAULT 'light',
      isRemembered BOOLEAN DEFAULT FALSE
    );
    """
    create_data_table = """
    CREATE TABLE IF NOT EXISTS Data (
      DID SERIAL PRIMARY KEY,
      UID INT NOT NULL,
      name VARCHAR(100),
      gpa FLOAT DEFAULT 0,
      FOREIGN KEY (UID) REFERENCES Users(UID) ON DELETE CASCADE
    );
    """
    create_data_low_table = """
    CREATE TABLE IF NOT EXISTS DataLow (
      DIDL SERIAL PRIMARY KEY,
      DID INT NOT NULL,
      courseName VARCHAR(100),
      grade FLOAT,
      credits FLOAT,
      FOREIGN KEY (DID) REFERENCES Data(DID) ON DELETE CASCADE
    );
    """

    cur.execute(create_users_table)
    cur.execute(create_data_table)
    cur.execute(create_data_low_table)

    conn.commit()
    cur.close()
    conn.close()
