from main import create_table, add_user
import pytest

@pytest.mark.parametrize("name, birthday, gender, fetish", [
    ("Anna", "1990-01-01", "Female", "none"),
    ("Bob", "1985-12-31", "Male", "kink"),
    ("", "2000-02-29", "Other", ""),
    ("LongNameUserThatIsReallyReallyLong", "1970-07-07", "Male", "some fetish text here"),
])
def test_add_user(db_connection, name, birthday, gender, fetish):
    add_user(db_connection, name, birthday, gender, fetish)

    cursor = db_connection.cursor()
    cursor.execute("SELECT name, birthday, gender, fetish FROM users WHERE name = %s", (name,))
    row = cursor.fetchone()
    
    # Проверяем, что данные записались и совпадают
    assert row is not None
    assert row[0] == name
    assert str(row[1]) == birthday  # birthday в базе - date, приводим к строке
    assert row[2] == gender
    assert row[3] == fetish
