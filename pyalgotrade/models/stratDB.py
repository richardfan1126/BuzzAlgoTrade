from pony.orm import Database, db_session, PrimaryKey, Required, Optional, sql_debug, db_session
from pony.orm.core import EntityMeta

from pyalgotrade.models import obj

import json

class StratDB():
    def __init__(self, user, password, host, database):
        self.db = Database("mysql", user = user, passwd = password, host = host, db = database)
        sql_debug(False)
        
        # TransRecord
        attrs = {}
        attrs['id'] = PrimaryKey(int, auto=True)
        attrs['strategy'] = Optional(str)
        attrs['symbol'] = Optional(str)
        attrs['secType'] = Optional(str)
        attrs['exchange'] = Optional(str)
        attrs['expiry'] = Optional(str)
        attrs['datetime'] = Optional(str)
        attrs['action'] = Optional(str)
        attrs['price'] = Optional(str)
        attrs['expiry'] = Optional(str)
        
        self.TransRecord = EntityMeta('TransRecord', (self.db.Entity,), attrs)
        
        # Record
        attrs = {}
        attrs['id'] = PrimaryKey(int, auto=True)
        attrs['strategy'] = Optional(str)
        attrs['symbol'] = Optional(str)
        attrs['secType'] = Optional(str)
        attrs['exchange'] = Optional(str)
        attrs['expiry'] = Optional(str)
        attrs['longPos'] = Optional(str)
        attrs['shortPos'] = Optional(str)
        attrs['entryPriceLong'] = Optional(str)
        attrs['entryPriceShort'] = Optional(str)
        attrs['curr_order_id'] = Optional(str)
        attrs['has_order'] = Optional(bool)
        
        self.Record = EntityMeta('Record', (self.db.Entity,), attrs)
        
        self.db.generate_mapping(create_tables=True)
    
    @db_session
    def setTransRecord(self, dt, act, p, strategy, symbol, secType, exchange, expiry):
        record = self.TransRecord(
            datetime = dt,
            action = act,
            price = p,
            strategy = strategy,
            symbol = symbol,
            secType = secType,
            exchange = exchange,
            expiry = expiry)

        commit()
    
    @db_session
    def checkOrCreateRecord(self, strategy, symbol, secType, exchange, expiry):
        if Record.exists(
            strategy = strategy,
            symbol = symbol,
            secType = secType,
            exchange = exchange,
            expiry = expiry):
            return
        else:
            record = Record(
                strategy = strategy,
                symbol = symbol,
                secType = secType,
                exchange = exchange,
                expiry = expiry,
                longPos = '',
                shortPos = '',
                has_order = 0)
            commit()
    
    @db_session
    def resetRecord(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record = queryObj[0]
    
        record.longPos = ''
        record.shortPos = ''
        record.entryPriceLong = ''
        record.entryPriceShort = ''
        record.has_order = 0
        commit()
    
    @db_session
    def setLongPos(self, longPos, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        record.longPos = longPos
        commit()
    
    @db_session
    def setShortPos(self, shortPos, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        record.shortPos = shortPos
        commit()
    
    @db_session
    def setEntryPriceLong(self, entryPriceLong, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        record.entryPriceLong = entryPriceLong
        commit()
    
    @db_session
    def setEntryPriceShort(self, entryPriceShort, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        record.entryPriceShort = entryPriceShort
        commit()
    
    
    @db_session
    def setCurrOrderID(self, order_id, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
        record=queryObj[0]
        record.curr_order_id = order_id
        commit()
    
    @db_session
    def setHasOrder(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        record.has_order = True
        commit()
    
    @db_session
    def removeHasOrder(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        record.has_order = False
        commit()
    
    @db_session
    def getHasOrder(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        return record.has_order
    
    @db_session
    def getLongPos(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        return record.longPos
    
    @db_session
    def getShortPos(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        return record.shortPos
    
    @db_session
    def getEntryPriceLong(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        return record.entryPriceLong
    
    @db_session
    def getEntryPriceShort(self, strategy, symbol, secType, exchange, expiry):
        queryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        return record.entryPriceShort
    
    @db_session
    def getCurrOrderID(self, strategy, symbol, secType, exchange, expiry):
        rqueryObj = select(p for p in Record if (
            p.strategy == strategy and p.symbol == symbol and p.secType == secType and p.exchange == exchange and p.expiry == expiry
        ))[:1]
        record=queryObj[0]
        return record.curr_order_id
