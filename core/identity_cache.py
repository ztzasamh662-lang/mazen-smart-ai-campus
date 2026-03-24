identity_cache = {}

CACHE_TIMEOUT = 10


def store_identity(tracking_id, person_id, timestamp):
    identity_cache[tracking_id] = {
        "person_id": person_id,
        "timestamp": timestamp
    }


def get_identity(tracking_id, current_time):

    if tracking_id not in identity_cache:
        return None

    data = identity_cache[tracking_id]

    if current_time - data["timestamp"] > CACHE_TIMEOUT:
        del identity_cache[tracking_id]
        return None

    return data["person_id"]