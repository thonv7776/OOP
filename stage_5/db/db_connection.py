"""
Database Connection Management
Handles MySQL connection setup and teardown for XAMPP.
"""

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """Manages MySQL database connection."""

    def __init__(self, host="localhost", user="root", password="", database="oop_db"):
        """
        Initialize database connection parameters.
        
        Args:
            host (str): Database host (default: localhost for XAMPP)
            user (str): Database user (default: root for XAMPP)
            password (str): Database password (default: empty for XAMPP)
            database (str): Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✓ Connected to database: {self.database}")
            return True
        except Error as e:
            print(f"✗ Connection failed: {e}")
            return False

    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Disconnected from database")

    def get_connection(self):
        """Get current database connection."""
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection

    def get_cursor(self):
        """Get cursor for executing queries."""
        return self.get_connection().cursor(dictionary=True)

    def commit(self):
        """Commit changes to database."""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback changes to database."""
        if self.connection:
            self.connection.rollback()

    def close_cursor(self, cursor):
        """Close cursor after use."""
        if cursor:
            cursor.close()


# Global database instance
db = DatabaseConnection()
