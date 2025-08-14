from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from main import connect_db, create_table, add_user, delete_user

app = Flask(__name__)

def init_db():
    conn = connect_db()
    create_table(conn)
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = connect_db()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        birthday = request.form.get('birthday', '').strip()
        gender = request.form.get('gender', '').strip()
        preference = request.form.get('preference', '').strip()

        if name and birthday and gender:
            add_user(conn, name, birthday, gender, preference)
        return redirect(url_for('index'))

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, birthday, gender, preference FROM users")
    users = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head><title>Users</title></head>
    <body>
      <h2>Users</h2>
      <h3>Add User</h3>
      <form method="POST" action="{{ url_for('index') }}">
        <input name="name" placeholder="Name" required>
        <input name="birthday" type="date" placeholder="Birthday" required>
        <input name="gender" placeholder="Gender" required>
        <input name="preference" placeholder="Preference">
        <button type="submit">Add</button>
      </form>

      <table border="1" cellpadding="5" cellspacing="0">
        <tr>
          <th>ID</th><th>Name</th><th>Birthday</th><th>Gender</th><th>Preference</th><th>Delete</th>
        </tr>
        {% for user in users %}
        <tr>
          <td>{{ user[0] }}</td>
          <td>{{ user[1] }}</td>
          <td>{{ user[2] }}</td>
          <td>{{ user[3] }}</td>
          <td>{{ user[4] }}</td>
          <td>
            <form method="POST" action="{{ url_for('delete_user_route', user_id=user[0]) }}" style="margin:0;">
              <button type="submit">Delete</button>
            </form>
          </td>
        </tr>
        {% endfor %}
      </table>
    </body>
    </html>
    """
    return render_template_string(html, users=users)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    conn = connect_db()
    delete_user(conn, user_id)
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
