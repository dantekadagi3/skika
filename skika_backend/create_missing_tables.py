#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skika_backend.settings')
django.setup()

from django.db import connection

def create_missing_tables():
    with connection.cursor() as cursor:
        # Create Ward table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ward (
                id UUID PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                constituency VARCHAR(100) DEFAULT 'Gatundu North',
                county VARCHAR(100) DEFAULT 'Kiambu',
                population_estimate INTEGER,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(name, constituency)
            );
        """)
        print("✓ Created ward table")
        
        # Create AuditLog table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id UUID PRIMARY KEY,
                user_id UUID NOT NULL REFERENCES core_user(id) ON DELETE CASCADE,
                action_type VARCHAR(20) NOT NULL,
                table_name VARCHAR(100) NOT NULL,
                record_id UUID NOT NULL,
                description TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        print("✓ Created audit_log table")
        
        # Create Notification table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notification (
                id UUID PRIMARY KEY,
                recipient_phone VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                status VARCHAR(10) DEFAULT 'pending',
                trigger_event VARCHAR(30) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                sent_at TIMESTAMP WITH TIME ZONE
            );
        """)
        print("✓ Created notification table")
        
        # Create index on audit_log timestamp for ordering
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS audit_log_timestamp_idx 
            ON audit_log (timestamp DESC);
        """)
        print("✓ Created audit_log index")

if __name__ == "__main__":
    create_missing_tables()
    print("\n✅ All missing tables created successfully!")