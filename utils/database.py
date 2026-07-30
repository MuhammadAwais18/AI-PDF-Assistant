import os
import sqlite3


DATABASE_NAME = "data/chat_history.db"


def get_connection():

    """
    Create database connection.
    """

    os.makedirs(
        "data",
        exist_ok=True
    )

    return sqlite3.connect(
        DATABASE_NAME
    )


def create_database():

    """
    Create chat history table.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT NOT NULL,

            answer TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()


def save_chat(question, answer):

    """
    Save conversation into database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO history
        (
            question,
            answer
        )

        VALUES (?, ?)
        """,
        (
            question,
            answer
        )
    )

    connection.commit()

    connection.close()


def get_history(limit=20):

    """
    Fetch previous conversations.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            question,
            answer,
            created_at

        FROM history

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            limit,
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def clear_history():

    """
    Delete all chat history.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM history
        """
    )

    connection.commit()

    connection.close()