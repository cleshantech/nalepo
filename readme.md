import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection utility
db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/charity_db")

def get_connection():
    return psycopg2.connect(db_url, cursor_factory=RealDictCursor)

# ------------------ FETCH QUERIES ------------------

def fetch_all_users(conn):
    """Return a list of all users."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, email, role, created_at FROM users;"
        )
        return cur.fetchall()


def fetch_user_by_id(conn, user_id):
    """Return a single user by ID."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, email, role, created_at FROM users WHERE id = %s;",
            (user_id,)
        )
        return cur.fetchone()


def fetch_all_campaigns(conn):
    """Return all campaigns."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, title, description, goal_amount, start_date, end_date, created_at FROM campaigns;"
        )
        return cur.fetchall()


def fetch_campaign_by_id(conn, campaign_id):
    """Return campaign details by ID."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM campaigns WHERE id = %s;",
            (campaign_id,)
        )
        return cur.fetchone()


def fetch_donations_by_campaign(conn, campaign_id):
    """Return donations for a specific campaign."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM donations WHERE campaign_id = %s ORDER BY donation_date DESC;",
            (campaign_id,)
        )
        return cur.fetchall()


def fetch_donations_by_user(conn, user_id):
    """Return donations made by a specific user."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM donations WHERE user_id = %s ORDER BY donation_date DESC;",
            (user_id,)
        )
        return cur.fetchall()


def fetch_all_volunteers(conn):
    """Return all volunteer signups."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM volunteers;")
        return cur.fetchall()


def fetch_all_events(conn):
    """Return all events."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM events ORDER BY event_date;")
        return cur.fetchall()


def fetch_event_registrations(conn, event_id):
    """Return registrations for a given event."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM event_registrations WHERE event_id = %s;",
            (event_id,)
        )
        return cur.fetchall()


def fetch_all_blog_posts(conn):
    """Return all blog posts."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM blog_posts ORDER BY published_at DESC;")
        return cur.fetchall()


def fetch_contact_messages(conn, unread_only=False):
    """Return contact messages, optionally only unread ones."""
    with conn.cursor() as cur:
        if unread_only:
            cur.execute("SELECT * FROM contact_messages WHERE is_read = FALSE;")
        else:
            cur.execute("SELECT * FROM contact_messages;")
        return cur.fetchall()


def fetch_payments_for_donation(conn, donation_id):
    """Return payment records for a specific donation."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM payments WHERE donation_id = %s ORDER BY paid_at DESC;",
            (donation_id,)
        )
        return cur.fetchall()

# ------------------ INSERT QUERIES ------------------

def insert_user(conn, name, email, password_hash, role='donor'):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s) RETURNING id;",
            (name, email, password_hash, role)
        )
        return cur.fetchone()["id"]


def insert_campaign(conn, title, description, goal_amount, start_date, end_date):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO campaigns (title, description, goal_amount, start_date, end_date) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (title, description, goal_amount, start_date, end_date)
        )
        return cur.fetchone()["id"]


def insert_donation(conn, user_id, campaign_id, amount, status='pending'):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO donations (user_id, campaign_id, amount, status) VALUES (%s, %s, %s, %s) RETURNING id;",
            (user_id, campaign_id, amount, status)
        )
        return cur.fetchone()["id"]


def insert_payment(conn, donation_id, provider, payment_reference, amount, status, paid_at=None, metadata=None):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO payments (donation_id, provider, payment_reference, amount, status, paid_at, metadata) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
            (donation_id, provider, payment_reference, amount, status, paid_at, metadata)
        )
        return cur.fetchone()["id"]


def insert_volunteer(conn, user_id, skills, availability):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO volunteers (user_id, skills, availability) VALUES (%s, %s, %s) RETURNING id;",
            (user_id, skills, availability)
        )
        return cur.fetchone()["id"]


def insert_event(conn, title, description, event_date, location):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO events (title, description, event_date, location) VALUES (%s, %s, %s, %s) RETURNING id;",
            (title, description, event_date, location)
        )
        return cur.fetchone()["id"]


def insert_event_registration(conn, event_id, user_id, status='registered'):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO event_registrations (event_id, user_id, status) VALUES (%s, %s, %s) RETURNING id;",
            (event_id, user_id, status)
        )
        return cur.fetchone()["id"]


def insert_blog_post(conn, author_id, title, content, published_at=None):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO blog_posts (author_id, title, content, published_at) VALUES (%s, %s, %s, COALESCE(%s, NOW())) RETURNING id;",
            (author_id, title, content, published_at)
        )
        return cur.fetchone()["id"]


def insert_contact_message(conn, name, email, message):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s) RETURNING id;",
            (name, email, message)
        )
        return cur.fetchone()["id"]

# Ensure to commit your transactions after using these functions, e.g.:
# conn = get_connection()
# try:
#     user_id = insert_user(conn, ...)
#     conn.commit()
# finally:
#     conn.close()
