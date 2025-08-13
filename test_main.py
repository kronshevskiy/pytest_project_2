from main import add_user, delete_user
import pytest

@pytest.mark.parametrize("name, birthday, gender, fetish", [
    ("Anna", "1990-01-01", "Female", "none"),
    ("Bob", "1985-12-31", "Male", "kink"),
    ("", "2000-02-29", "Other", ""),
    ("LongNameUserThatIsReallyReallyLong", "1970-07-07", "Male", "some fetish text here"),
])
def test_add_user(db_connection, name, birthday, gender, fetish):
    # 1. Добавляем пользователя
    add_user(db_connection, name, birthday, gender, fetish)

    # 2. Достаём этого пользователя из базы
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT name, birthday, gender, fetish FROM users WHERE name = %s",
        (name,)
    )
    row = cursor.fetchone()

    # 3. Проверяем каждое поле по отдельности
    assert row is not None
    assert row[0] == name            # имя
    assert str(row[1]) == birthday   # дата (привели к строке)
    assert row[2] == gender          # пол
    assert row[3] == fetish          # фетиш



