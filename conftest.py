import pytest
import mysql.connector

@pytest.fixture(scope="session")
def db_connection():
    print("\n[SETUP] Подключаемся к БД")
    conn = mysql.connector.connect(
        host="localhost",
        user="test_user",
        database="test_db",
    )
    yield conn
    print("\n[TEARDOWN] Закрываем подключение к БД")
    conn.close()
