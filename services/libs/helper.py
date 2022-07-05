import uuid
from datetime import datetime
def generate_unique_uuid():
    return str(uuid.uuid4())

def get_current_datetime():
    return datetime.now()