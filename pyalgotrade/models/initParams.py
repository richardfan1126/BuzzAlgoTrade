from __future__ import absolute_import, print_function

from decimal import Decimal
from pony.orm import *

import json

class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

db = Database("sqlite", "initParams.sqlite", create_db=True)

class InitParam(db.Entity):
    id = PrimaryKey(int, auto=True)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)

    param_set_name = Optional(str)
    extra_params = Optional(str)

    hibernate_start_time = Optional(str)
    hibernate_end_time = Optional(str)
    balance_trade_start_time = Optional(str)
    balance_trade_end_time = Optional(str)
    stop_loss_long = Optional(float)
    stop_loss_short = Optional(float)
    stop_profit_long = Optional(float)
    stop_profit_short = Optional(float)

sql_debug(False)
db.generate_mapping(create_tables=True)


# ------- TFA Param functions
@db_session
def setParam(symbol, secType, exchange, hibernate_start_time, hibernate_end_time, balance_trade_start_time, balance_trade_end_time, stop_loss_long , stop_loss_short , stop_profit_long , stop_profit_short, param_set_name, **extra_params):
    extra_params = json.dumps(extra_params)

    if InitParam.exists(symbol = symbol,
                        secType = secType,
                        exchange = exchange,
                        param_set_name = param_set_name):
        record = InitParam.get(symbol = symbol,
                               secType = secType,
                               exchange = exchange,
                               param_set_name = param_set_name)

        record.extra_params = extra_params

        record.hibernate_start_time = hibernate_start_time
        record.hibernate_end_time = hibernate_end_time
        record.balance_trade_start_time = balance_trade_start_time
        record.balance_trade_end_time = balance_trade_end_time
        record.stop_loss_long = stop_loss_long
        record.stop_loss_short = stop_loss_short
        record.stop_profit_long = stop_profit_long
        record.stop_profit_short = stop_profit_short
    else:
        record = InitParam(symbol = symbol,
                           secType = secType,
                           exchange = exchange,
                           extra_params = extra_params,
                           hibernate_start_time = hibernate_start_time,
                           hibernate_end_time = hibernate_end_time,
                           balance_trade_start_time = balance_trade_start_time,
                           balance_trade_end_time = balance_trade_end_time,
                           stop_loss_long = stop_loss_long,
                           stop_loss_short = stop_loss_short,
                           stop_profit_long = stop_profit_long,
                           stop_profit_short = stop_profit_short,
                           param_set_name = param_set_name)
    commit()

@db_session
def getParam(symbol, secType, exchange, param_set_name):
    if InitParam.exists(symbol = symbol,
                        secType = secType,
                        exchange = exchange,
                        param_set_name = param_set_name):
        record = InitParam.get(symbol = symbol,
                               secType = secType,
                               exchange = exchange,
                               param_set_name = param_set_name)

        return_record = record.to_dict()
        extra_params = json.loads(record.extra_params)
        
        for key in extra_params:
            return_record[key] = extra_params[key]

        return obj(return_record)
    else:
        return None
