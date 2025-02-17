import sqlite3

keyword = input("Enter a keyword to search for: ")

conn = sqlite3.connect("flashcards.db")
cursor = conn.cursor()
cursor.execute('SELECT * FROM flashcards WHERE front LIKE ? OR back LIKE ?', (f'%{keyword}%', f'%{keyword}%'))
results = cursor.fetchall()
conn.close()

for card in results:
    print(f"ID: {card[0]}, Front: {card[1]}, Back: {card[2]}")
