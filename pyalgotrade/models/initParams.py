from pony.orm import Database, db_session, PrimaryKey, Required, Optional, sql_debug
from pony.orm.core import EntityMeta

from pyalgotrade.models import obj

import json

class InitParam():
    def __init__(self, user, password, host, database):
        self.db = Database("mysql", user = user, passwd = password, host = host, db = database)
        sql_debug(False)
        
        attrs = {}
        attrs['id'] = PrimaryKey(int, auto=True)
        attrs['symbol'] = Optional(str)
        attrs['secType'] = Optional(str)
        attrs['exchange'] = Optional(str)
    
        attrs['param_set_name'] = Optional(str)
        attrs['extra_params'] = Optional(str)
    
        attrs['hibernate_start_time'] = Optional(str)
        attrs['hibernate_end_time'] = Optional(str)
        attrs['balance_trade_start_time'] = Optional(str)
        attrs['balance_trade_end_time'] = Optional(str)
        attrs['stop_loss_long'] = Optional(float)
        attrs['stop_loss_short'] = Optional(float)
        attrs['stop_profit_long'] = Optional(float)
        attrs['stop_profit_short'] = Optional(float)
        
        self.InitParam = EntityMeta('InitParam', (self.db.Entity,), attrs)
        self.db.generate_mapping(create_tables=True)

    @db_session
    def setParam(self, symbol, secType, exchange, hibernate_start_time, hibernate_end_time, balance_trade_start_time, balance_trade_end_time, stop_loss_long , stop_loss_short , stop_profit_long , stop_profit_short, param_set_name, **extra_params):
        extra_params = json.dumps(extra_params)
    
        if self.InitParam.exists(symbol = symbol,
                            secType = secType,
                            exchange = exchange,
                            param_set_name = param_set_name):
            record = self.InitParam.get(symbol = symbol,
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
            record = self.InitParam(symbol = symbol,
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
    def getParam(self, symbol, secType, exchange, param_set_name):
        if self.InitParam.exists(symbol = symbol,
                            secType = secType,
                            exchange = exchange,
                            param_set_name = param_set_name):
            record = self.InitParam.get(symbol = symbol,
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
