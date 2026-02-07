"""
Canteen Rush AI - Multi-Vendor Marketplace
Production-Ready Database Layer (REFACTORED)
"""

import sqlite3
import random
from contextlib import contextmanager
from datetime import datetime

DB_FILE = "canteen.db"

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize all tables with robust migrations."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                roll_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                pin TEXT NOT NULL,
                points INTEGER DEFAULT 100
            )
        """)
        
        # 2. Vendors Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                image_url TEXT
            )
        """)

        # 3. Admins Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # 4. Menu Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                price INTEGER NOT NULL,
                avg_prep_time INTEGER NOT NULL,
                image_url TEXT,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (vendor_id) REFERENCES vendors(id)
            )
        """)
        
        # 5. Orders Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                student_name TEXT, -- Legacy support
                vendor_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                status TEXT DEFAULT 'Received',
                order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                predicted_pickup_time TEXT,
                FOREIGN KEY (user_id) REFERENCES users(roll_no),
                FOREIGN KEY (vendor_id) REFERENCES vendors(id)
            )
        """)
        
        # --- MIGRATIONS ---
        try: cursor.execute("ALTER TABLE users ADD COLUMN points INTEGER DEFAULT 100")
        except: pass

        try: cursor.execute("ALTER TABLE orders ADD COLUMN student_name TEXT")
        except: pass

        cursor.execute("PRAGMA table_info(orders)")
        cols = [r[1] for r in cursor.fetchall()]
        if "student_id" in cols and "user_id" not in cols:
            cursor.execute("ALTER TABLE orders RENAME COLUMN student_id TO user_id")
            
        # --- SEED DATA ---
        cursor.execute("SELECT COUNT(*) FROM vendors")
        if cursor.fetchone()[0] == 0:
            vendors = [
                ("Grill Master", "grill", "123", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=300"),
                ("Fresh Brew", "coffee", "123", "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300"),
                ("Noodles & Co", "noodle", "123", "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=300")
            ]
            cursor.executemany("INSERT INTO vendors (name, username, password, image_url) VALUES (?, ?, ?, ?)", vendors)
        
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ("admin", "admin123"))

        cursor.execute("SELECT COUNT(*) FROM menu")
        if cursor.fetchone()[0] == 0:
            items = [
                (1, "Classic Burger", 120, 10, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300"),
                (1, "BBQ Chicken", 180, 15, "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=300"),
                (1, "Grilled Sandwich", 90, 8, "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=300"),
                (2, "Cappuccino", 60, 5, "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300"),
                (2, "Cold Brew", 80, 6, "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=300"),
                (2, "Croissant", 70, 3, "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=300"),
                (3, "Pad Thai", 150, 12, "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=300"),
                (3, "Ramen Bowl", 160, 14, "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=300"),
                (3, "Spring Rolls", 80, 7, "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300")
            ]
            cursor.executemany("INSERT INTO menu (vendor_id, item_name, price, avg_prep_time, image_url) VALUES (?, ?, ?, ?, ?)", items)
        
        conn.commit()

# --- REFACTORED FUNCTIONS ---

def register_user(roll_no, name, pin):
    try:
        with get_db() as conn:
            conn.execute("INSERT INTO users (roll_no, name, pin, points) VALUES (?, ?, ?, 100)", (roll_no.strip(), name.strip(), pin))
            conn.commit()
            return True
    except sqlite3.IntegrityError: return False

def verify_user(roll_no, pin):
    with get_db() as conn:
        row = conn.execute("SELECT name, points FROM users WHERE roll_no = ? AND pin = ?", (roll_no.strip(), pin)).fetchone()
        return dict(row) if row else None

def verify_vendor(username, password):
    with get_db() as conn:
        row = conn.execute("SELECT id, name FROM vendors WHERE username = ? AND password = ?", (username, password)).fetchone()
        return dict(row) if row else None

def verify_admin(username, password):
    with get_db() as conn:
        row = conn.execute("SELECT id FROM admins WHERE username = ? AND password = ?", (username, password)).fetchone()
        return True if row else False

def get_item_prep_time_by_name(item_name):
    with get_db() as conn:
        row = conn.execute("SELECT avg_prep_time FROM menu WHERE item_name = ?", (item_name,)).fetchone()
        return row["avg_prep_time"] if row else 5

def check_ban_status(roll_no):
    with get_db() as conn:
        row = conn.execute("SELECT points FROM users WHERE roll_no = ?", (roll_no.strip(),)).fetchone()
        return row["points"] < 40 if row else False

def get_user_points(roll_no):
    with get_db() as conn:
        row = conn.execute("SELECT points FROM users WHERE roll_no = ?", (roll_no.strip(),)).fetchone()
        return row["points"] if row else 0

def deduct_points(roll_no, amount=10):
    with get_db() as conn:
        conn.execute("UPDATE users SET points = MAX(0, points - ?) WHERE roll_no = ?", (amount, roll_no.strip()))
        conn.commit()
        return True

def get_all_vendors():
    with get_db() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM vendors").fetchall()]

def get_menu(vendor_id, active_only=True):
    with get_db() as conn:
        query = "SELECT * FROM menu WHERE vendor_id = ?" + (" AND is_active = 1" if active_only else "")
        return [dict(r) for r in conn.execute(query, (vendor_id,)).fetchall()]

def toggle_item_availability(item_id, status):
    with get_db() as conn:
        conn.execute("UPDATE menu SET is_active = ? WHERE id = ?", (1 if status else 0, item_id))
        conn.commit()

def add_order(user_id, vendor_id, item_name, prediction):
    token_id = f"#VR-{random.randint(100, 999)}"
    with get_db() as conn:
        user_row = conn.execute("SELECT name FROM users WHERE roll_no = ?", (user_id.strip(),)).fetchone()
        name = user_row["name"] if user_row else "Unknown"
        cols = [r[1] for r in conn.execute("PRAGMA table_info(orders)").fetchall()]
        if "student_name" in cols:
            conn.execute("""INSERT INTO orders (token_id, user_id, student_name, vendor_id, item_name, predicted_pickup_time)
                            VALUES (?, ?, ?, ?, ?, ?)""", (token_id, user_id.strip(), name, vendor_id, item_name, prediction))
        else:
            conn.execute("""INSERT INTO orders (token_id, user_id, vendor_id, item_name, predicted_pickup_time)
                            VALUES (?, ?, ?, ?, ?)""", (token_id, user_id.strip(), vendor_id, item_name, prediction))
        conn.commit()
        return token_id

def get_vendor_orders(vendor_id):
    with get_db() as conn:
        rows = conn.execute("""SELECT o.*, u.name as student_name 
                               FROM orders o JOIN users u ON o.user_id = u.roll_no
                               WHERE o.vendor_id = ? AND o.status NOT IN ('Collected', 'Expired')
                               ORDER BY o.order_time ASC""", (vendor_id,)).fetchall()
        return [dict(r) for r in rows]

def get_user_active_orders(user_id):
    with get_db() as conn:
        rows = conn.execute("""SELECT o.*, v.name as vendor_name 
                               FROM orders o JOIN vendors v ON o.vendor_id = v.id
                               WHERE o.user_id = ? AND o.status NOT IN ('Collected', 'Expired')
                               ORDER BY o.order_time DESC""", (user_id.strip(),)).fetchall()
        return [dict(r) for r in rows]

def get_vendor_active_orders_count(vendor_id):
    with get_db() as conn:
        return conn.execute("SELECT COUNT(*) FROM orders WHERE vendor_id = ? AND status NOT IN ('Collected', 'Expired')", (vendor_id,)).fetchone()[0]

def update_status(order_id, new_status):
    with get_db() as conn:
        conn.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()

def expire_order_with_penalty(order_id):
    with get_db() as conn:
        order = conn.execute("SELECT user_id FROM orders WHERE id = ?", (order_id,)).fetchone()
        if order:
            conn.execute("UPDATE orders SET status = 'Expired' WHERE id = ?", (order_id,))
            conn.execute("UPDATE users SET points = MAX(0, points - 10) WHERE roll_no = ?", (order['user_id'],))
            conn.commit()
            pts = conn.execute("SELECT points FROM users WHERE roll_no = ?", (order['user_id'],)).fetchone()['points']
            return True, order['user_id'], pts
        return False, None, 0
