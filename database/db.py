import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


class Database:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            self.connect()

    def connect(self):
        """Create PostgreSQL connection (singleton)"""
        if Database._connection is not None:
            return

        try:
            Database._connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                cursor_factory=RealDictCursor
            )

            Database._cursor = Database._connection.cursor()
            print("✅ Connected to PostgreSQL")

        except Exception as e:
            print(f"❌ Database Connection Error: {e}")
            Database._connection = None
            Database._cursor = None

    @property
    def connection(self):
        return Database._connection

    @property
    def cursor(self):
        return Database._cursor

    def execute(self, query, values=None):
        """Execute INSERT, UPDATE, DELETE"""
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"Execution Error: {e}")
            raise

    def fetchone(self, query, values=None):
        """Return one row"""
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Fetch One Error: {e}")
            raise

    def fetchall(self, query, values=None):
        """Return all rows"""
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Fetch All Error: {e}")
            raise

    def close(self):
        """Close database connection (singleton)"""
        if Database._cursor:
            Database._cursor.close()
            Database._cursor = None

        if Database._connection:
            Database._connection.close()
            Database._connection = None
            print("Database connection closed")