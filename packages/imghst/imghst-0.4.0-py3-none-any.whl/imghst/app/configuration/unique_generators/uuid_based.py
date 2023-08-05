import uuid


def generate_unique_id(*args, **kwargs) -> str:
    return str(uuid.uuid4().hex[:6])
