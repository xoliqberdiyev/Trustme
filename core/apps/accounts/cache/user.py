import redis

from django.contrib.auth.hashers import make_password

from config.env import env

r = redis.StrictRedis.from_url(env.str('REDIS_URL'))


def cache_user_credentials(phone_number, password, time):
    hashed_password = make_password(password)
    key = f"user_credentials:{phone_number}"

    r.hmset(key, {
        "phone": phone_number,
        "password": hashed_password
    })

    r.expire(key, time)


def get_user_creadentials(phone_number):
    key = f"user_credentials:{phone_number}"
    data = r.hgetall(key)

    if not data:
        return None
    
    return {
        "phone": data.get(b"phone").decode() if data.get(b"phone") else None,
        "password": data.get(b"password").decode() if data.get(b"password") else None
    }