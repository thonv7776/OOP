"""
Database Package
Contains database connection and SQL operations for the Jukebox application.
"""

from db.db_connection import db, DatabaseConnection
from db import db_function

__all__ = ['db', 'DatabaseConnection', 'db_function']
