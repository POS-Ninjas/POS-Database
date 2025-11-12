from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import sqlite3


@dataclass
class DatabaseContext:
    db_path = Path('/home/test/Desktop/pos/POS-Database') / 'test.db'
    conn: Optional[sqlite3.Connection] = field(default=None, init=False)
    cursor: Optional[sqlite3.Cursor]   = field(default=None, init=False)

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, _exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
                print(f"Transaction failed: {exc_type.__name__}: {exc_val}")
            self.conn.close()
        return False
    
    def execute(self, query: str, params: tuple = ()):
        """Wrapper method that uses the stored cursor"""
        return self.cursor.execute(query, params)
    
    def fetchone(self):
        """Fetch from the stored cursor"""
        return self.cursor.fetchone() if self.cursor else None
    
    def fetchall(self):
        """Fetch from the stored cursor"""
        return self.cursor.fetchall() if self.cursor else []
    
    def drop_all_tables(self):
        return self.cursor.executemany




