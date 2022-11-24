import datetime
import time
import traceback
import logging
import dateutil
from config import Config as config
import jwt
from common.responses import failure
def get_time_stamp():
    try:
        obj = int(time.time())
        return obj
    except Exception as err:
        return None


def get_datetime():
    try:
        date_time = datetime.datetime.now().strftime(config.DATETIME_FORMAT)
        return date_time
    except Exception as err:
        return None


def get_timestamp_diff(timestamp):
    try:
        dt1 = datetime.datetime.fromtimestamp(get_time_stamp())
        dt2 = datetime.datetime.fromtimestamp(timestamp)
        dt_diff = dateutil.relativedelta.relativedelta(dt1, dt2)
        diff_in_minute = (dt1 - dt2) // datetime.timedelta(minutes=1)
        # log.info("In Minutes", diff_in_minute)
        # log.info("Difference", dt_diff.days, dt_diff.hours, dt_diff.minutes, dt_diff.seconds)
        return diff_in_minute
    except Exception as err:
        return None


def get_auth_exp(timeout_in_minutes):
    try:
        ts = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout_in_minutes)
        return ts
    except Exception as err:
        logging.exception(traceback.print_exc())
        return None



def createToken(u_id):
    try:
        payload = u_id
        identity = {'identity': payload, "exp": get_auth_exp(config.JWT_TOKEN_TIME_OUT_IN_MINUTES)}
        print(identity)
        token = jwt.encode(identity, config.SECRET_KEY, config.JWT_ALGORITHM)
        tk = token

        refres_identity = {'identity': payload, "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES)}
        refres_token = jwt.encode(refres_identity, config.SECRET_KEY, config.JWT_ALGORITHM)
        refres_tk = refres_token
        token = {'token': str(tk), 'refresh_token':str(refres_tk), 'user_id': u_id}
        return token
    except Exception as err:
        print(traceback.print_exc())
        return failure(str(err))