import sqlite3
import hashlib
import secrets
import hmac
import os
import json
import re
from datetime import datetime, timedelta

# ==========================================================
# DATABASE PATH
# ==========================================================
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skillgap_users.db")
LEGACY_USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

# ==========================================================
# CRYPTOGRAPHIC SECURITY HELPERS
# ==========================================================
PBKDF2_ITERATIONS = 200000

def hash_password_secure(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hashes password using PBKDF2-HMAC-SHA256 with 200,000 iterations.
    Returns (hash_hex, salt).
    """
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        PBKDF2_ITERATIONS
    )
    return key.hex(), salt

def verify_password_secure(password: str, stored_hash: str, salt: str) -> bool:
    """Constant-time verification of password against stored PBKDF2 hash."""
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        PBKDF2_ITERATIONS
    )
    return hmac.compare_digest(key.hex(), stored_hash)

def legacy_sha256_hash(password: str) -> str:
    """Legacy unsalted SHA-256 for backwards compatibility with users.json."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password_strength(password: str) -> tuple[int, str]:
    """
    Evaluates password strength:
    Returns (score 0-100, label: 'Weak' | 'Medium' | 'Strong' | 'Excellent')
    """
    if not password:
        return 0, "Empty"
    score = 0
    if len(password) >= 6:
        score += 25
    if len(password) >= 10:
        score += 15
    if re.search(r"[a-z]", password):
        score += 15
    if re.search(r"[A-Z]", password):
        score += 15
    if re.search(r"[0-9]", password):
        score += 15
    if re.search(r"[@$!%*#?&^()_+={}\[\]:;<>,.?~\\/-]", password):
        score += 15

    score = min(score, 100)
    if score < 40:
        label = "Weak"
    elif score < 70:
        label = "Medium"
    elif score < 90:
        label = "Strong"
    else:
        label = "Excellent"
    return score, label

# ==========================================================
# DATABASE INITIALIZATION & SCHEMA
# ==========================================================
def get_db_connection():
    """Returns a SQLite connection with row_factory set to sqlite3.Row."""
    conn = sqlite3.connect(DB_FILE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes tables, indexes, and migrates legacy users if present."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL COLLATE NOCASE,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT DEFAULT 'Student',
            target_role TEXT DEFAULT 'Full Stack Developer',
            experience_level TEXT DEFAULT 'Entry Level',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            login_count INTEGER DEFAULT 0,
            failed_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)

    # 2. Login Audit Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            identifier TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT,
            attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    # 3. Password Reset Tokens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL COLLATE NOCASE,
            reset_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0
        )
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_login_audit_time ON login_audit(attempt_time)")

    conn.commit()

    # Seed Default Demo Accounts
    _seed_default_accounts(cursor)
    conn.commit()

    # Migrate from legacy users.json
    _migrate_legacy_users(cursor)
    conn.commit()

    conn.close()

def _seed_default_accounts(cursor):
    """Seed ready-to-use demo accounts for students and recruiters."""
    defaults = [
        {
            "email": "demo@skillgap.ai",
            "username": "demo_student",
            "full_name": "Demo Student",
            "password": "Password123!",
            "role": "Student",
            "target_role": "Full Stack Developer",
            "experience_level": "Undergraduate / Fresher"
        },
        {
            "email": "alex@skillgap.ai",
            "username": "alex_rivera",
            "full_name": "Alex Rivera",
            "password": "Password123!",
            "role": "Professional",
            "target_role": "Senior Frontend Engineer",
            "experience_level": "2+ Years Experience"
        },
        {
            "email": "priya@skillgap.ai",
            "username": "priya_sharma",
            "full_name": "Priya Sharma",
            "password": "Password123!",
            "role": "Researcher",
            "target_role": "AI / Machine Learning Engineer",
            "experience_level": "Postgraduate / Specialist"
        }
    ]

    for d in defaults:
        cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", (d["email"], d["username"]))
        if not cursor.fetchone():
            p_hash, p_salt = hash_password_secure(d["password"])
            cursor.execute("""
                INSERT INTO users (email, username, full_name, password_hash, salt, role, target_role, experience_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (d["email"], d["username"], d["full_name"], p_hash, p_salt, d["role"], d["target_role"], d["experience_level"]))

def _migrate_legacy_users(cursor):
    """Migrates any users stored in users.json into the SQLite database."""
    if not os.path.exists(LEGACY_USER_FILE):
        return

    try:
        with open(LEGACY_USER_FILE, "r") as f:
            data = json.load(f)
        for username, user_obj in data.items():
            email = username if "@" in username else f"{username}@skillgap.local"
            cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
            if not cursor.fetchone():
                stored_hash = user_obj.get("password", "")
                # Stored as legacy sha256. We'll store it with a special marker salt 'LEGACY_SHA256'
                cursor.execute("""
                    INSERT INTO users (email, username, full_name, password_hash, salt, role, target_role)
                    VALUES (?, ?, ?, ?, ?, 'Student', 'Software Engineer')
                """, (email, username, username.capitalize(), stored_hash, "LEGACY_SHA256"))
    except Exception:
        pass

# ==========================================================
# AUTHENTICATION & USER MANAGEMENT API
# ==========================================================

def register_user_db(email: str, password: str, full_name: str = "", username: str = "", target_role: str = "Full Stack Developer", experience_level: str = "Entry Level") -> tuple[bool, str]:
    """
    Registers a new user in the SQLite database.
    Enforces format checks, uniqueness, and PBKDF2 hashing.
    """
    email = email.strip().lower()
    password = password.strip()
    full_name = full_name.strip()
    username = username.strip().lower() if username.strip() else email.split("@")[0]

    if not email or "@" not in email:
        return False, "Please provide a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not full_name:
        full_name = username.capitalize()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check uniqueness
        cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email or username already exists."

        p_hash, p_salt = hash_password_secure(password)
        cursor.execute("""
            INSERT INTO users (email, username, full_name, password_hash, salt, target_role, experience_level, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Student')
        """, (email, username, full_name, p_hash, p_salt, target_role, experience_level))

        user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO login_audit (user_id, identifier, status, message)
            VALUES (?, ?, 'SUCCESS', 'Account registered successfully')
        """, (user_id, email))

        conn.commit()
        conn.close()
        return True, "Account registered successfully! You may now sign in."
    except Exception as e:
        conn.close()
        return False, f"Registration error: {str(e)}"

def authenticate_user_db(identifier: str, password: str) -> tuple[bool, dict | str]:
    """
    Authenticates a user against the SQLite database by email or username.
    Protects against brute force with account lockout after 5 consecutive failures.
    Returns (True, user_dict) on success, or (False, error_message) on failure.
    """
    identifier = identifier.strip().lower()
    password = password.strip()

    if not identifier or not password:
        return False, "Please enter both identifier and password."

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE email = ? OR username = ?
    """, (identifier, identifier))
    user = cursor.fetchone()

    if not user:
        cursor.execute("""
            INSERT INTO login_audit (identifier, status, message)
            VALUES (?, 'FAILED', 'User not found')
        """, (identifier,))
        conn.commit()
        conn.close()
        return False, "Invalid email/username or password."

    user_dict = dict(user)

    # Check Lockout Status
    if user_dict.get("locked_until"):
        try:
            lock_time = datetime.fromisoformat(user_dict["locked_until"])
            if datetime.now() < lock_time:
                rem_mins = int((lock_time - datetime.now()).total_seconds() / 60) + 1
                conn.close()
                return False, f"Account locked due to 5 failed attempts. Please retry in {rem_mins} minute(s)."
            else:
                # Lock expired, reset
                cursor.execute("UPDATE users SET locked_until = NULL, failed_attempts = 0 WHERE id = ?", (user_dict["id"],))
                conn.commit()
        except Exception:
            pass

    # Verify Password
    stored_hash = user_dict["password_hash"]
    salt = user_dict["salt"]
    is_valid = False

    if salt == "LEGACY_SHA256":
        # Check against legacy SHA-256
        if legacy_sha256_hash(password) == stored_hash:
            is_valid = True
            # Automatically upgrade to PBKDF2
            new_hash, new_salt = hash_password_secure(password)
            cursor.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, user_dict["id"]))
    else:
        is_valid = verify_password_secure(password, stored_hash, salt)

    if is_valid:
        # Successful login
        now_str = datetime.now().isoformat()
        cursor.execute("""
            UPDATE users
            SET last_login = ?,
                login_count = login_count + 1,
                failed_attempts = 0,
                locked_until = NULL
            WHERE id = ?
        """, (now_str, user_dict["id"]))

        cursor.execute("""
            INSERT INTO login_audit (user_id, identifier, status, message)
            VALUES (?, ?, 'SUCCESS', 'Authenticated successfully')
        """, (user_dict["id"], identifier))

        conn.commit()
        # Fetch updated user record
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_dict["id"],))
        updated_user = dict(cursor.fetchone())
        # Remove sensitive hash/salt from returned dict
        updated_user.pop("password_hash", None)
        updated_user.pop("salt", None)
        conn.close()
        return True, updated_user
    else:
        # Failed login attempt tracking
        fails = user_dict.get("failed_attempts", 0) + 1
        lock_until_val = None
        if fails >= 5:
            lock_until_val = (datetime.now() + timedelta(minutes=15)).isoformat()
            msg = "Account locked for 15 minutes due to 5 failed attempts."
        else:
            msg = f"Invalid password. Attempt {fails} of 5 before lockout."

        cursor.execute("""
            UPDATE users
            SET failed_attempts = ?,
                locked_until = ?
            WHERE id = ?
        """, (fails, lock_until_val, user_dict["id"]))

        cursor.execute("""
            INSERT INTO login_audit (user_id, identifier, status, message)
            VALUES (?, ?, 'FAILED', ?)
        """, (user_dict["id"], identifier, msg))

        conn.commit()
        conn.close()
        return False, msg

def reset_password_db(email: str, new_password: str) -> tuple[bool, str]:
    """Resets user password in SQLite database with secure PBKDF2 hash."""
    email = email.strip().lower()
    new_password = new_password.strip()

    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "No account found matching this email address."

    new_hash, new_salt = hash_password_secure(new_password)
    cursor.execute("""
        UPDATE users
        SET password_hash = ?,
            salt = ?,
            failed_attempts = 0,
            locked_until = NULL
        WHERE id = ?
    """, (new_hash, new_salt, user["id"]))

    cursor.execute("""
        INSERT INTO login_audit (user_id, identifier, status, message)
        VALUES (?, ?, 'RESET', 'Password reset successfully')
    """, (user["id"], email))

    conn.commit()
    conn.close()
    return True, "Password has been successfully updated! You can now sign in."

def get_database_stats() -> dict:
    """Returns database telemetry and statistics."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM login_audit WHERE status = 'SUCCESS'")
        login_count = cursor.fetchone()[0]

        cursor.execute("SELECT email, full_name, role, target_role, created_at, last_login FROM users ORDER BY id DESC LIMIT 5")
        recent_users = [dict(r) for r in cursor.fetchall()]

        conn.close()

        size_kb = os.path.getsize(DB_FILE) / 1024 if os.path.exists(DB_FILE) else 0

        return {
            "total_users": user_count,
            "total_successful_logins": login_count,
            "recent_users": recent_users,
            "db_size_kb": round(size_kb, 2),
            "db_path": os.path.basename(DB_FILE),
            "status": "Healthy & Connected"
        }
    except Exception as e:
        return {
            "total_users": 0,
            "total_successful_logins": 0,
            "recent_users": [],
            "db_size_kb": 0,
            "db_path": os.path.basename(DB_FILE),
            "status": f"Error: {str(e)}"
        }

# Automatically initialize database schema on module import
init_db()
