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

def check_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print("Existing tables in database:")
        for table in tables:
            print(f"  - {table}")
        
        # Check specifically for core app tables
        core_tables = [table for table in tables if any(
            model_name in table.lower() 
            for model_name in ['user', 'report', 'notification', 'audit_log', 'project', 'feedback']
        )]
        
        print(f"\nCore app related tables ({len(core_tables)}):")
        for table in core_tables:
            print(f"  - {table}")

if __name__ == "__main__":
    check_tables()