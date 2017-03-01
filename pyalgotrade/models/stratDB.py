from __future__ import absolute_import, print_function

from decimal import Decimal
from pony.orm import *

db = Database("sqlite", "stratDB.sqlite", create_db=True)

class SignalRecordBCR(db.Entity):
    id = PrimaryKey(int, auto=True)
    datetime = Optional(str)
    signalType = Optional(str)
    signal = Optional(str)
    checkPrice = Optional(str)
    macd = Optional(str)
    slv = Optional(str)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)

class SignalRecordTFS(db.Entity):
    id = PrimaryKey(int, auto=True)
    datetime = Optional(str)
    signalType = Optional(str)
    fast_sma = Optional(str)
    slow_sma = Optional(str)
    rsi = Optional(str)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)

class SignalRecordTFC(db.Entity):
    id = PrimaryKey(int, auto=True)
    datetime = Optional(str)
    signalType = Optional(str)
    fast_sma = Optional(str)
    slow_sma = Optional(str)
    cci = Optional(str)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)

class SignalRecordMRA(db.Entity):
    id = PrimaryKey(int, auto=True)
    datetime = Optional(str)
    signalType = Optional(str)
    sma_CO_1 = Optional(str)
    sma_highlow_1 = Optional(str)
    sma_close_1 = Optional(str)
    sma_CO_2 = Optional(str)
    sma_highlow_2 = Optional(str)
    sma_close_2 = Optional(str)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)

class SignalRecordYCO(db.Entity):
    id = PrimaryKey(int, auto=True)
    datetime = Optional(str)
    signalType = Optional(str)
    highlow = Optional(str)
    longshortcheck = Optional(str)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)

class Record(db.Entity):
    id = PrimaryKey(int, auto=True)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)
    longPos = Optional(str)
    shortPos = Optional(str)
    entryPriceLong = Optional(str)
    entryPriceShort = Optional(str)
    curr_order_id = Optional(str)
    has_order = Optional(bool)


class TransRecord(db.Entity):
    id = PrimaryKey(int, auto=True)
    strategy = Optional(str)
    symbol = Optional(str)
    secType = Optional(str)
    exchange = Optional(str)
    expiry = Optional(str)
    datetime = Optional(str)
    action = Optional(str)
    price = Optional(str)
    expiry = Optional(str)

sql_debug(False)
db.generate_mapping(create_tables=True)



@db_session
def resetRecord(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]

    record.longPos = ''
    record.shortPos = ''
    record.entryPriceLong = ''
    record.entryPriceShort = ''
    record.has_order = 0
    commit()

@db_session
def setTransRecord(dt,act,p, strategy, symbol, secType, exchange, expiry):
    record = TransRecord(datetime=dt,action=act,price=p, strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry)

    commit()

@db_session
def checkOrCreateRecord(strategy, symbol, secType, exchange, expiry):
    if Record.exists(strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry):
        print('Has Record. Proceed programme.')
    else:
        record = Record(strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry, longPos='', shortPos='', has_order=0)
        print('Create Record. Proceed programme.')
    commit()

@db_session
def setLongPos(longPos, strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.longPos = longPos
    commit()

@db_session
def setShortPos(shortPos, strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.shortPos = shortPos
    commit()

@db_session
def setEntryPriceLong(entryPriceLong, strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.entryPriceLong = entryPriceLong
    commit()

@db_session
def setEntryPriceShort(entryPriceShort, strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.entryPriceShort = entryPriceShort
    commit()


@db_session
def setCurrOrderID(order_id, strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.curr_order_id = order_id
    commit()

@db_session
def setHasOrder(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.has_order = True
    commit()

@db_session
def removeHasOrder(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    record.has_order = False
    commit()

@db_session
def getHasOrder(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    return record.has_order

@db_session
def getLongPos(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    return record.longPos

@db_session
def getShortPos(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    return record.shortPos

@db_session
def getEntryPriceLong(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    return record.entryPriceLong

@db_session
def getEntryPriceShort(strategy, symbol, secType, exchange, expiry):
    queryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    return record.entryPriceShort

@db_session
def getCurrOrderID(strategy, symbol, secType, exchange, expiry):
    rqueryObj = select(p for p in Record if (p.strategy==strategy and p.symbol==symbol and p.secType==secType and p.exchange==exchange and p.expiry==expiry))[:1]
    record=queryObj[0]
    return record.curr_order_id

@db_session
def setSignalRecordMRA(dt, sigT, sco1, sh1, sc1, sco2, sh2, sc2, strategy, symbol, secType, exchange, expiry):
    record = SignalRecordMRA(datetime=dt, signalType=sigT, sma_CO_1=sco1, sma_highlow_1=sh1, sma_close_1=sc1, sma_CO_2=sco2, sma_highlow_2=sh2, sma_close_2=sc2, strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry)
    commit()

@db_session
def setSignalRecordTFS(dt, sigT, fs, ss, r, strategy, symbol, secType, exchange, expiry):
    record = SignalRecordTFS(datetime=dt, signalType=sigT, fast_sma=fs, slow_sma=ss, rsi=r, strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry)
    commit()

@db_session
def setSignalRecordTFC(dt, sigT, fs, ss, r, strategy, symbol, secType, exchange, expiry):
    record = SignalRecordTFC(datetime=dt, signalType=sigT, fast_sma=fs, slow_sma=ss, cci=r, strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry)
    commit()

@db_session
def setSignalRecordBCR(dt, sigT, sig, cp, m, s, strategy, symbol, secType, exchange, expiry):
    record = SignalRecordBCR(datetime=dt, signalType=sigT, signal=sig, checkPrice=cp, macd=m, slv=s, strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry)
    commit()

@db_session
def setSignalRecordYCO(dt, sigT, hl, lsc, strategy, symbol, secType, exchange, expiry):
    record = SignalRecordYCO(datetime=dt, signalType=sigT, highlow=hl, longshortcheck=lsc, strategy=strategy, symbol=symbol, secType=secType, exchange=exchange, expiry=expiry)
    commit()
