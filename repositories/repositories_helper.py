import copy
import datetime
import uuid
import jwt
import logging
import os
import json
import hashlib

DBPATH = "/Users/thdg/PycharmProjects/eWalletv1/ewallet.db"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def uuid_generator():
    return str(uuid.uuid4())


def signature_generator(key, **kwargs):
    kwargs.pop('signature', None)
    kwargs['key'] = key
    to_encode = json.dumps(kwargs)
    rs = hashlib.md5(to_encode.encode())
    return rs.hexdigest()


def check_signature(key, **kwargs):
    rs = signature_generator(key, **kwargs)
    if rs == kwargs['signature']:
        return True
    return False


def token_decode(token, api_key=None):
    if api_key:
        return jwt.decode(token, api_key, algorithms=["HS256"])
    return jwt.decode(token, options={"verify_signature": False})


def logging_helper():
    def setup_logger():
        time = datetime.datetime.now()

        file_name = os.path.join(DIR_PATH, f"{str(time.date())}.log")

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)

        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(c_handler)
        return logger
