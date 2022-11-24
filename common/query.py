import traceback
from config import db
from sqlalchemy import text


def add_item(obj):
    try:
        db.session.add(obj)
        db.session.commit()
        return obj
    except Exception as err:
        # db.session.rollback()
        # log.exception(traceback.print_exc())
        return None

def raw_select(sql):
    try:
        result_proxy = raw_execution(sql)
        result = []
        if result_proxy:
            for row in result_proxy:
                row_as_dict = dict(row)
                date_ = row_as_dict.values()
                result.append(row_as_dict)
            result_proxy.close()
            return result
        else:
            return result
    except Exception as err:
        # logging.exception(traceback.print_exc())
        return []


def raw_execution(sql):
    try:
        result = db.engine.execute(text(sql).execution_options(autocommit=True))
        return result
    except Exception as err:
        # log.exception(traceback.print_exc())
        # print(traceback.print_exc())
        return None