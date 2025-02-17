import sqlite3

front = input("Enter the front of the flashcard: ")
back = input("Enter the back of the flashcard: ")

conn = sqlite3.connect("flashcards.db")
cursor = conn.cursor()
cursor.execute('INSERT INTO flashcards (front, back) VALUES (?, ?)', (front, back))
conn.commit()
conn.close()

print("Flashcard added successfully.")

