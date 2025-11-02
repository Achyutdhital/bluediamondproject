#!/usr/bin/env python3
"""
Quick script to fix indentation in settings.py
Run this on the server if settings.py has indentation errors
"""
import sys
import os

def fix_settings_indentation(filepath):
    """Read settings.py and convert all tabs to 4 spaces"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tabs with 4 spaces
        fixed_content = content.replace('\t', '    ')
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✓ Fixed indentation in {filepath}")
        print("  Converted all tabs to spaces")
        return True
        
    except Exception as e:
        print(f"✗ Error fixing {filepath}: {e}")
        return False

if __name__ == '__main__':
    # Use provided path or default
    if len(sys.argv) > 1:
        settings_path = sys.argv[1]
    else:
        settings_path = '/home/camhsano/bluediamondservice/core/core/settings.py'
    
    if not os.path.exists(settings_path):
        print(f"Error: File not found: {settings_path}")
        print("Usage: python fix_settings_indent.py [path/to/settings.py]")
        sys.exit(1)
    
    if fix_settings_indentation(settings_path):
        print("\nNow restart your app:")
        print("  touch /home/camhsano/bluediamondservice/tmp/restart.txt")
        sys.exit(0)
    else:
        sys.exit(1)
