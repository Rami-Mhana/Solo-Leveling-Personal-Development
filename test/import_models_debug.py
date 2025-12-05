import traceback
try:
    from app import models
    print('Imported app.models OK')
except Exception:
    traceback.print_exc()
