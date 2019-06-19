import os
import datetime

MONGO_URI = os.environ.get("MONGO_URI")
JWT_SECRET_KEY = os.environ.get("SECRET")
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
