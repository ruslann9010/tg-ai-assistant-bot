import aiosqlite
from typing import List, Dict


class DatabaseService:
    """A service class responsible for managing asynchronous SQLite database operations.
    
    This class handles the initialization of the database schema, as well as 
    storing and retrieving contextual user chat histories for the AI bot.
    """

    def __init__(self, db_path: str = "database.db"):
        """Initializes the database service with a specific database file path.

        Args:
            db_path (str): The file path to the SQLite database. Defaults to "database.db".
        """
        self.db_path = db_path


    async def init_db(self) -> None:
        """Asynchronously initializes the database by creating necessary tables.

        Creates the `messages` table if it does not already exist. This table 
        stores individual message threads with structural metadata required for 
        maintaining conversation history.

        Schema Details:
            - id (INTEGER): Auto-incrementing primary key.
            - user_id (INTEGER): Unique identifier of the Telegram user.
            - role (TEXT): Represents the sender type ('system', 'user', or 'assistant').
            - content (TEXT): The actual text content of the message.
            - timestamp (DATETIME): Automatic generation of the record creation time.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    role TEXT,
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()


    async def save_message(self, user_id: int, role: str, content: str) -> None:
        """Asynchronously persists a new message log into the database.

        Appends a conversational record from either the user or the AI assistant 
        to track individual chat contexts. Uses parameterized queries to avoid 
        SQL injection.

        Args:
            user_id (int): Unique Telegram identifier of the target user.
            role (str): Context type indicator. Must be 'user' or 'assistant'.
            content (str): Raw string containing the text payload of the message.
        """

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)", (user_id, role, content)
                )
            await db.commit()


    async def get_context(self, user_id: int, limit: int = 10) -> List[Dict[str, str]]:
        """Retrieves conversational history for a user formatted for the AI SDK.

        Extracts the last N interactions from the storage layer, reverses their 
        sequence to build an accurate chronological window, and maps them 
        into structure representations expected by GigaChat.

        Args:
            user_id (int): Unique Telegram identifier of the target user.
            limit (int, optional): Maximum window size of latest messages to fetch. 
                Defaults to 10.

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing message 
                payloads. Example format:
                [
                    {"role": "user", "content": "Hello!"},
                    {"role": "assistant", "content": "Hi there! How can I help you?"}
                ]
        """

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT role, content FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?", 
                (user_id, limit)) 
            rows = await cursor.fetchall()
            await cursor.close()

        clean_rows = [tuple(row) for row in rows]
        return [{"role": r, "content": c} for r, c in reversed(clean_rows)]


    async def clear_context(self, user_id: int) -> None:
        """Asynchronously purges the conversation history for a specific user.

        Removes all stored messages associated with the given user ID from the 
        database. This is typically invoked via user commands like /clear or 
        /reset to wipe the AI assistant's memory window.

        Args:
            user_id (int): Unique Telegram identifier of the target user whose 
                history needs to be deleted.
        """
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM messages WHERE user_id = ?", [user_id])
            await db.commit()       
