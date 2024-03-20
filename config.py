import os

class DevConfig():
    MONGODB_SETTINGS = {
        "db": os.gentenv('MONGODB_DB'),
        "host": os.gentenv('MONGODB_HOST'),
        "username": os.gentenv('MONGODB_USER'),
        "password": os.gentenv('MONGODB_PASSWORD'),
      }
