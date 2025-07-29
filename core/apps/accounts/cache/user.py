import redis

from django.contrib.auth.hashers import make_password

from config.env import env

r = redis.StrictRedis.from_url(env.str('REDIS_URL'))


def cache_user_credentials(phone_number, password, first_name, last_name, email, time):
    key = f"user_credentials:{phone_number}"

    r.hmset(key, {
        "phone": phone_number,
        "password": password,
        "first_name": first_name, 
        "last_name": last_name, 
        "email": email
    })

    r.expire(key, time)


def get_user_creadentials(phone_number):
    key = f"user_credentials:{phone_number}"
    data = r.hgetall(key)

    if not data:
        return None
    
    return {
        "phone": data.get(b"phone").decode() if data.get(b"phone") else None,
        "password": data.get(b"password").decode() if data.get(b"password") else None,
        "first_name": data.get(b"first_name").decode() if data.get(b'first_name') else None,
        "last_name": data.get(b"last_name").decode() if data.get(b'last_name') else None,
        "email": data.get(b"email").decode() if data.get(b'email') else None,
    }