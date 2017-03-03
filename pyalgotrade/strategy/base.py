import logging

from pyalgotrade.models.stratDB import StratDB

class BaseIBTradeStrategy():
    debug = False
    
    db_username = None
    db_password = None
    db_host = None
    db_database = None
    
    current_stat= ''
    symbol = ''
    sec_type = ''
    exchange = ''
    expiry = ''
    
    strat_db = None
    
    early_buy = False
    
    def __init__(self):
        logging.basicConfig(level = logging.INFO, filename = self.current_stat + '_' + self.symbol + '_log.txt')
        
        self.__init_strat_db()
    
    def __init_strat_db(self):
        self.strat_db = StratDB(self.db_username, self.db_password, self.db_host, self.db_database)
    
    def pre_run(self):
        self.__long_pos = self.strat_db.getLongPos(self.current_stat, self.symbol, self.sec_type, self.exchange, self.expiry)
        
        if self.debug:
            print self.__long_pos
            
        if self.__long_pos == "":
            self.__long_pos = ""
        else:
            self.__long_pos = 1

        self.__short_pos = self.strat_db.getShortPos(self.current_stat, self.symbol, self.sec_type, self.exchange, self.expiry)
        
        if self.debug:
            print self.__short_pos
        
        if self.__short_pos == "":
            self.__short_pos = ""
        else:
            self.__short_pos = 1

        self.__sell_bool = False
        self.__buy_bool = False
    
    def early_check(self, original, high, low):
        if original[0] and low[0] and high[0]:
            self.__sell_bool = True
            self.early_buy = True
        elif original[1] and low[1] and high[1]:
            self.__buy_bool = True
            self.early_buy = True

    def late_check(self, original):
        if original[0]:
            self.__sell_bool = True
        elif original[1]:
            self.__buy_bool = True

    def get_action(self):
        if self.strat_db.getHasOrder(CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY):
            if self.debug:
                print 'Has Order in Queue... cannot place new'
            return None
        
        if self.__long_pos == "" and self.__short_pos == "":
            if self.debug:
                print 'waiting buy/sell'

            if not self.is_in_trade_time() or self.in_exit_market_time():
                if self.debug:
                    print 'Not in trade time'
                return None
            
            if self.__sell_bool:
                if self.debug:
                    print 'First SELL'
                
                return 'sell_short'

            if self.__buy_bool:
                if self.debug:
                    print 'First BUY'
                
                return 'buy_long'

        elif self.__long_pos != "" and self.__short_pos == "":
            if self.is_in_no_trade_time():
                if self.__sell_bool:
                    if self.debug:
                        logging.info("stop converting and exit long")
                    
                    return 'quit_buy'
            
            if self.debug:
                print 'waiting for changeHand buy -> sell'
            
            if self.__sell_bool:
                if not self.is_in_trade_time():
                    if self.debug:
                        print 'Not in trade time'
                    return None 

                if self.debug:
                    print 'changeHand buy -> sell'
                return 'change_hand_buy'
            
        elif self.__long_pos == "" and self.__short_pos != "":
            if self.is_in_no_trade_time():
                if self.__buy_bool:
                    if self.debug:
                        logging.info("stop converting and exit short")
                    
                    return 'quit_sell'
            
            if self.debug:
                print 'waiting for changeHand sell -> buy'
            
            if self.__buy_bool:
                if not self.is_in_trade_time():
                    if self.debug:
                        print 'Not in trade time'
                    return None
                
                if self.debug:
                    print 'changeHand sell -> buy'
                return 'change_hand_sell'
            
        elif self.__long_pos != "" and self.__short_pos != "":
            if self.debug:
                logging.info("both is not none")
            
            return None    

    def time_in_range(self, start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def buyLong(self):
        self.__long_pos = 1
        makeOrder("BUY", 1)
        self.strat_db.setLongPos("1", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)

    def sellShort(self):
        self.__short_pos=1
        makeOrder("SELL",1)
        self.strat_db.setShortPos("1", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)

    def changeHand(self, original):
        if original=="BUY":
            self.__long_pos=""
            self.__short_pos=1
            makeOrder("SELL",2)
            self.strat_db.setLongPos("", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
            self.strat_db.setShortPos("1", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
            self.strat_db.setEntryPriceLong("",CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
        elif original=="SELL":
            self.__short_pos=""
            self.__long_pos=1
            makeOrder("BUY",2)
            self.strat_db.setLongPos("1", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
            self.strat_db.setShortPos("", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
            self.strat_db.setEntryPriceShort("",CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)

    def quitMarket(self, status):
        if status=="BUY":
            self.__long_pos=""
            makeOrder("SELL",1)
            self.strat_db.setLongPos("", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
            self.strat_db.setEntryPriceLong("",CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
        elif status=="SELL":
            self.__short_pos=""
            makeOrder("BUY",1)
            self.strat_db.setShortPos("", CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)
            self.strat_db.setEntryPriceShort("",CURR_STRAT, SYMBOL, SEC_TYPE, EXCHANGE, EXPIRY)

    def isOvernight(self, st, ed):
        if datetime.datetime.strptime(st,"%H:%M").time() < datetime.datetime.strptime(ed,"%H:%M").time():
            return False
        else:
            return True

    def is_in_trade_time(self):
        if self.isOvernight(hibernate_start_time, hibernate_end_time):
            if time_in_range(datetime.datetime.strptime(hibernate_start_time+":00","%H:%M:%S").time(), datetime.datetime.strptime("23:59:59","%H:%M:%S").time(),server_time.time()) or\
            time_in_range(datetime.datetime.strptime("00:00:00","%H:%M:%S").time(), datetime.datetime.strptime(hibernate_end_time+":00","%H:%M:%S").time(),server_time.time()):
                return False
            else:
                return True
        else:
            if time_in_range(datetime.datetime.strptime(hibernate_start_time+":00","%H:%M:%S").time(), datetime.datetime.strptime(hibernate_end_time+":00","%H:%M:%S").time(),server_time.time()):
                return False
            else:
                return True

    def in_exit_market_time(self):
        if self.time_in_range(datetime.datetime.strptime(balance_trade_end_time+":00","%H:%M:%S").time(), datetime.datetime.strptime(balance_trade_end_time+":59","%H:%M:%S").time(),datetime.datetime.now().time()):
            return True
        else:
            return False
        return False

    def is_in_no_trade_time(self):
        if self.time_in_range(datetime.datetime.strptime(balance_trade_start_time,"%H:%M").time(), datetime.datetime.strptime(balance_trade_end_time,"%H:%M").time(), datetime.datetime.now().time()):
            return True
        else:
            return False
