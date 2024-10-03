from .general import  SECRET_KEY
import os
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL_CHANNEL","redis://localhost:6379/0")],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}
