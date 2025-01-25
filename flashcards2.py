#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, run, template, request, redirect
import sqlite3

# Initialize Bottle app
app = Bottle()


def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            front TEXT,
            back TEXT,
            memorized BOOLEAN DEFAULT 0,
            compartment INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return template('''
        <h1>Flashcards</h1>
        <button onclick="window.location='/study'">Study</button>
        <button onclick="window.location='/add'">Add Card</button>
        <button onclick="window.location='/search'">Search Card</button>
    ''')


@app.route('/add', method=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        front = request.forms.get('front')
        back = request.forms.get('back')
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO flashcards (front, back) VALUES (?, ?)',
                       (front, back))
        conn.commit()
        conn.close()
        return redirect('/')
    return template('''
        <h1>Add Flashcard</h1>
        <form method="post">
            <label>Front:</label><br>
            <textarea name="front"></textarea><br>
            <label>Back:</label><br>
            <textarea name="back"></textarea><br>
            <button type="submit">Add</button>
        </form>
    ''')


@app.route('/search', method=['GET', 'POST'])
def search_card():
    if request.method == 'POST':
        keyword = request.forms.get('keyword')
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM flashcards WHERE front LIKE ? OR back LIKE ?',
            (f'%{keyword}%', f'%{keyword}%'))
        results = cursor.fetchall()
        conn.close()
        return template('''
            <h1>Search Results</h1>
            % for card in results:
                <p><b>Front:</b> {{!card[1]}}</p>
                <p><b>Back:</b> {{!card[2]}}</p>
                <a href="/edit/{{card[0]}}">Edit</a><br>
            % end
            <a href="/">Back to menu</a>
        ''',
                        results=results)
    return template('''
        <h1>Search Flashcards</h1>
        <form method="post">
            <label>Keyword:</label><br>
            <input type="text" name="keyword"><br>
            <button type="submit">Search</button>
        </form>
    ''')


@app.route('/study', method=['GET', 'POST'])
def study():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM flashcards WHERE memorized = 0 ORDER BY compartment ASC LIMIT 1'
    )
    card = cursor.fetchone()
    conn.close()
    if card:
        return template('''
            <h1>Study Flashcard</h1>
            <p><b>Front:</b> {{!card[1]}}</p>
            <form method="post" action="/flip/{{card[0]}}">
                <button type="submit">Flip</button>
            </form>
            <a href="/">Back to menu</a>
        ''',
                        card=card)
    return '<h1>No cards to study!</h1><a href="/">Back to menu</a>'


@app.route('/flip/<card_id>', method=['POST'])
def flip(card_id):
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flashcards WHERE id = ?', (card_id, ))
    card = cursor.fetchone()
    conn.close()
    if card:
        return template('''
            <h1>Study Flashcard</h1>
            <p><b>Back:</b> {{!card[2]}}</p>
            <form method="post" action="/memorize/{{card[0]}}">
                <button type="submit">Mark as Memorized</button>
            </form>
            <form method="post" action="/not_memorized/{{card[0]}}">
                <button type="submit">Mark as Not Memorized</button>
            </form>
            <a href="/edit/{{card[0]}}">Edit</a><br>
            <a href="/">Back to menu</a>
        ''',
                        card=card)
    return redirect('/study')


@app.route('/memorize/<card_id>', method='POST')
def memorize(card_id):
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE flashcards SET memorized = 1, compartment = compartment + 1 WHERE id = ?',
        (card_id, ))
    conn.commit()
    conn.close()
    return redirect('/study')


@app.route('/not_memorized/<card_id>', method='POST')
def not_memorized(card_id):
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE flashcards SET memorized = 0 WHERE id = ?',
                   (card_id, ))
    conn.commit()
    conn.close()
    return redirect('/study')


@app.route('/edit/<card_id>', method=['GET', 'POST'])
def edit_card(card_id):
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        front = request.forms.get('front')
        back = request.forms.get('back')
        cursor.execute(
            'UPDATE flashcards SET front = ?, back = ? WHERE id = ?',
            (front, back, card_id))
        conn.commit()
        conn.close()
        return redirect('/')
    cursor.execute('SELECT * FROM flashcards WHERE id = ?', (card_id, ))
    card = cursor.fetchone()
    conn.close()
    return template('''
        <h1>Edit Flashcard</h1>
        <form method="post">
            <label>Front:</label><br>
            <textarea name="front">{{!card[1]}}</textarea><br>
            <label>Back:</label><br>
            <textarea name="back">{{!card[2]}}</textarea><br>
            <button type="submit">Save</button>
        </form>
    ''',
                    card=card)


if __name__ == "__main__":
    init_db()
    run(app, host='localhost', port=8080)
