import traceback
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from app import create_app
    print('Imported create_app OK')
except Exception as e:
    print('Import failed:')
    traceback.print_exc()
