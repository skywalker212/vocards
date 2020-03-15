""" Our own tiny ORM """
# using lightweight sqlite database, perfect for our purpose
import sqlite3
from datetime import datetime
import time

def create_words_table():
    try:
        conn = sqlite3.connect("vocab.db")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS WORDS
        (WORD           CHAR(50)        PRIMARY KEY     NOT NULL,
        ADDITION_DATE   INT             NOT NULL,
        COUNT           INT             DEFAULT 1);
        ''')
        print("Words table created successfully!")
        conn.commit()
        cursor.close()
    except sqlite3.Error as e:
        print("some error occured:", e.args[0])

def drop_words_table():
    try:
        conn = sqlite3.connect("vocab.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS WORDS")
        print("Words table dropped successfully!")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("some error occured:", e.args[0])

def insert_words(word_list):
    try:
        conn = sqlite3.connect("vocab.db")
        # need to do this whole conversion cause we only want the UTC timestamp accurate to the date, not to the actual hours/seconds/miliseconds/...
        todays_date = datetime.utcnow().strftime("%d/%m/%Y")
        todays_utc_seconds = time.mktime(datetime.strptime(todays_date, "%d/%m/%Y").timetuple())
        cursor = conn.cursor()
        words = [ (word, todays_utc_seconds, count) for (word, count) in word_counts(word_list, cursor) ]
        for (word, date, count) in words:
            if count:
                cursor.execute('UPDATE WORDS SET COUNT=? WHERE WORD=?', (count+1, word))
            else:
                cursor.execute('INSERT INTO WORDS (WORD, ADDITION_DATE) VALUES (?,?)', (word, date))
        print("Successfully inserted {} words in table".format(len(words)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("some error occured:", e.args[0])

def word_counts(word_list, cursor):
    for word in word_list:
        cursor.execute("SELECT COUNT FROM WORDS WHERE WORD=?", (word,))
        record = cursor.fetchone()
        if record:
            yield (word, record[0])
        else:
            yield (word, None)