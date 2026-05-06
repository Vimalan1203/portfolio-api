"""
CLI script to create an admin user in the database.

Usage:
    python create_admin.py
"""

import sys
import os
from datetime import datetime

# Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

from app.db.database import SessionLocal, engine
from app.models.portfolio_models import Base, User
from app.core.security import hash_password


def create_admin():
    # Ensure all tables exist (including users)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("=" * 40)
        print("   Create Admin User")
        print("=" * 40)

        username = input("Enter username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            sys.exit(1)

        email = input("Enter email: ").strip()
        if not email or "@" not in email:
            print("❌ Please enter a valid email.")
            sys.exit(1)

        import getpass
        password = getpass.getpass("Enter password: ")
        if len(password) < 6:
            print("❌ Password must be at least 6 characters.")
            sys.exit(1)

        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("❌ Passwords do not match.")
            sys.exit(1)

        # Check if username already exists
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing:
            print(f"❌ A user with that username or email already exists.")
            sys.exit(1)

        # Create the admin user
        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_admin=True,
            is_active=True,
            created_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print()
        print("✅ Admin user created successfully!")
        print(f"   Username : {admin.username}")
        print(f"   Email    : {admin.email}")
        print(f"   Is Admin : {admin.is_admin}")
        print(f"   Created  : {admin.created_at}")
        print()
        print("You can now login at POST /api/auth/login")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
