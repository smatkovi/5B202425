from bottle import route, run, template, request, static_file
import sqlite3

# Connect to the database
conn = sqlite3.connect('flashcards.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS flashcards
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              front TEXT, 
              back TEXT, 
              memorized BOOLEAN DEFAULT 0, 
              compartment INTEGER)''')
conn.commit()


@route('/')
def index():
    # Get all flashcards
    c.execute("SELECT * FROM flashcards")
    rows = c.fetchall()
    return template('index.tpl', flashcards=rows)


@route('/add', method='POST')
def add_flashcard():
    front = request.forms.get('front')
    back = request.forms.get('back')
    c.execute("INSERT INTO flashcards (front, back) VALUES (?, ?)",
              (front, back))
    conn.commit()
    return '<p>Flashcard added successfully!</p>'


@route('/review')
def review():
    # Get a random flashcard from compartment 1
    c.execute(
        "SELECT * FROM flashcards WHERE compartment=1 ORDER BY RANDOM() LIMIT 1"
    )
    row = c.fetchone()
    if row:
        return template('review.tpl', flashcard=row)
    else:
        return '<p>No flashcards in compartment 1.</p>'


@route('/answer', method='POST')
def answer():
    flashcard_id = int(request.forms.get('id'))
    is_correct = request.forms.get('is_correct')

    if is_correct == 'true':
        # Move to the next compartment
        current_compartment = c.execute(
            "SELECT compartment FROM flashcards WHERE id=?",
            (flashcard_id, )).fetchone()[0]
        new_compartment = min(current_compartment + 1, 5)
        c.execute("UPDATE flashcards SET compartment=? WHERE id=?",
                  (new_compartment, flashcard_id))
    else:
        # Move back to compartment 1
        c.execute("UPDATE flashcards SET compartment=1 WHERE id=?",
                  (flashcard_id, ))

    conn.commit()
    return review()


@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static')


# Define templates
index_tpl = '''<!DOCTYPE html>
<html>
<head>
    <title>Flashcards</title>
</head>
<body>
    <h1>Flashcards</h1>
    <form action="/add" method="POST">
        <label for="front">Front:</label>
        <input type="text" id="front" name="front"><br><br>
        <label for="back">Back:</label>
        <input type="text" id="back" name="back"><br><br>
        <input type="submit" value="Add Flashcard">
    </form>
    <h2>All Flashcards</h2>
    <table>
        <thead>
            <tr>
                <th>Front</th>
                <th>Back</th>
                <th>Compartment</th>
            </tr>
        </thead>
        <tbody>
            {% for flashcard in flashcards %}  <tr>
                <td>{{ flashcard[1] }}</td>  <td>{{ flashcard[2] }}</td>
                <td>{{ flashcard[4] }}</td>
            </tr>
            {% end %}
        </tbody>
    </table>
</body>
</html>
'''
