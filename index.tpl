<!DOCTYPE html>
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
