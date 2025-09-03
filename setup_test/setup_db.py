import sqlite3
import os

class IPDataBase:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, 'ip_data.db')
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        
    def create_table(self):
        # address 테이블이 없으면 생성
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                value TEXT NOT NULL
            );
        ''')
        self.conn.commit()
            
    def add_ip(self, ip_text):
        self.conn.execute('INSERT INTO addresses (type, value) VALUES (?, ?)', ('ip', ip_text))
        self.conn.commit()
        
    def add_touch_port(self, tp_text):
        self.conn.execute('INSERT INTO addresses (type, value) VALUES (?, ?)', ('tp', tp_text))
        self.conn.commit()
    
    def add_setup_port(self, sp_text):
        self.conn.execute('INSERT INTO addresses (type, value) VALUES (?, ?)', ('sp', sp_text))
        self.conn.commit()

    def get_all_ips(self):
        cursor = self.conn.execute('SELECT id, type, value FROM addresses')
        return cursor.fetchall()

    def delete_ip(self, ip_text):
        self.conn.execute(
            'DELETE FROM addresses WHERE type=? AND value=?', ('ip', ip_text)
            )
        self.conn.commit()

    def delete_tp(self, tp_text):
        self.conn.execute(
            'DELETE FROM addresses WHERE type=? AND value=?',('tp', tp_text)
            )
        self.conn.commit()

    def delete_sp(self, sp_text):
        self.conn.execute(
            'DELETE FROM addresses WHERE type=? AND value=?',('sp', sp_text)
            )
        self.conn.commit()

