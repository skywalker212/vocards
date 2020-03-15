""" Our own tiny ORM """
# using lightweight sqlite database, perfect for our purpose
import sqlite3

conn = sqlite3.connect("vocab.db")


def create_words_table():
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS WORDS
        (WORD           CHAR(50)        PRIMARY KEY     NOT NULL,
        ADDITION_DATE   INT             NOT NULL,
        COUNT      INT             DEFAULT 1       NOT NULL);
        ''')
        print("Words table created successfully!")
        cursor.close()
    except sqlite3.Error as e:
        print("some error occured:", e.args[0])

def drop_words_table():
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS WORDS")
        print("Words table dropped successfully!")
    except sqlite3.Error as e:
        print("some error occured:", e.args[0])