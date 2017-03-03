import datetime, time, sys

from ib.opt import Connection
from ib.ext.Contract import Contract

from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.feed import ib_data_feed 
from pyalgotrade.models.initParams import InitParam

class IBTradeStrategy():
    debug = False
    
    main_loop_interval = 0.2
    
    feed = None
    feed_high = None
    feed_low = None
    feed_late = None
    
    close_var = 2
    server_time = None
    last_time = None
    early_check = False
    early_buy = False
    
    initParam = None
    db_username = None
    db_password = None
    db_host = None
    db_database = None
    
    contract = None
    
    order_id = 1
    tracker_id = 1
    
    feed_frequency = 60
    min_feed_required = 54
    instrument_name = 'hsi'
    
    client_id = 1
    current_stat= ''
    symbol = ''
    sec_type = ''
    exchange = ''
    expiry = ''
    currency = ''
    param_set_name = ''
    
    def __init__(self, **kwargs):
        if 'client_id' in kwargs:
            self.client_id = kwargs['client_id']
        
        if 'current_stat' in kwargs:
            self.current_stat = kwargs['current_stat']
        
        if 'symbol' in kwargs:
            self.symbol = kwargs['symbol']
        
        if 'sec_type' in kwargs:
            self.sec_type = kwargs['sec_type']
        
        if 'exchange' in kwargs:
            self.exchange = kwargs['exchange']
        
        if 'expiry' in kwargs:
            self.expiry = kwargs['expiry']
        
        if 'currency' in kwargs:
            self.currency = kwargs['currency']
        
        if 'param_set_name' in kwargs:
            self.param_set_name = kwargs['param_set_name']
        
        if 'db_username' in kwargs:
            self.db_username = kwargs['db_username']
        
        if 'db_password' in kwargs:
            self.db_password = kwargs['db_password']
        
        if 'db_host' in kwargs:
            self.db_host = kwargs['db_host']
        
        if 'db_database' in kwargs:
            self.db_database = kwargs['db_database']
        
        self.tws = Connection.create(port = 7496, clientId = self.client_id)
        
        self.feed = ib_data_feed.IbDataFeed(self.feed_frequency)
        self.feed_high = ib_data_feed.IbDataFeed(self.feed_frequency)
        self.feed_low = ib_data_feed.IbDataFeed(self.feed_frequency)
        self.feed_late = ib_data_feed.IbDataFeed(self.feed_frequency)
    
    def historical_data_handler(self, msg):
        try:
            utc = datetime.datetime.strptime(msg.date, '%Y%m%d  %H:%M:%S')
        except ValueError:
            if self.debug:
                print 'price tick handler value error'
            return
    
        if msg.date[:8] != "finished":
            date = utc.strftime("%Y-%m-%d %H:%M:%S")
            server_time_check = self.server_time.replace(second = 0, microsecond = 0)
            bar_time_check = utc.replace(second = 0,microsecond = 0)
            if bar_time_check.time() != server_time_check.time():
                if self.early_check:
                    self.feed.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
                    self.feed_high.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
                    self.feed_low.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
                else:
                    self.feed_late.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
            elif bar_time_check.time() == server_time_check.time() and self.early_check:
                highClose = msg.close + self.close_var
                lowClose = msg.close - self.close_var
                if highClose > msg.high:
                    newHigh = highClose
                else:
                    newHigh = msg.high
                if lowClose < msg.low:
                    newLow = lowClose
                else:
                    newLow = msg.low
                    
                self.feed.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
                self.feed_high.addBar(date, msg.open, highClose, msg.low, newHigh, msg.volume)
                self.feed_low.addBar(date, msg.open, lowClose, newLow, msg.high, msg.volume)
        else:
            if self.early_check:
                self.feed.finishAddBar(self.instrument_name)
                self.feed_high.finishAddBar(self.instrument_name)
                self.feed_low.finishAddBar(self.instrument_name)
                
                if self.debug:
                    print 'feed count'
                    print self.feed.get_count()
                    print self.feed_high.get_count()
                    print self.feed_low.get_count()
                    
                if feed.get_count() >= self.min_feed_required:
                    self.run_strategy(True)
            else:
                self.feed_late.finishAddBar(self.instrument_name)
                
                if self.debug:
                    print 'feed count'
                    print self.feed_late.get_count()
                    
                if self.feed_late.get_count() >= self.min_feed_required:
                    self.run_strategy(False)
    
    def __load_param(self):
        self.init_param = InitParam(self.db_username, self.db_password, self.db_host, self.db_database)
        
        init_param_obj = self.init_param.getParam(self.symbol, self.sec_type, self.exchange, self.param_set_name)
        
        if not init_param_obj:
            sys.exit("No initiation param for your product. Check database initParams")
        else:
            fastSMA_size = init_param_obj.fastSMA_size
            slowSMA_size = init_param_obj.slowSMA_size
            RSI_size = init_param_obj.RSI_size
            rsi_low = init_param_obj.rsi_low
            rsi_high = init_param_obj.rsi_high
            hibernate_start_time = init_param_obj.hibernate_start_time
            hibernate_end_time = init_param_obj.hibernate_end_time
            balance_trade_start_time = init_param_obj.balance_trade_start_time
            balance_trade_end_time = init_param_obj.balance_trade_end_time
            stop_loss_long = init_param_obj.stop_loss_long
            stop_loss_short = init_param_obj.stop_loss_short
            stop_profit_long = init_param_obj.stop_profit_long
            stop_profit_short = init_param_obj.stop_profit_short
    
    def __connect_tws(self):
        self.tws.register(self.historical_data_handler, 'HistoricalData')
        self.tws.register(self.next_valid_id_handler, 'NextValidId')
        self.tws.register(self.order_status_handler, 'OrderStatus')
        self.tws.register(self.tick_price_handler, 'TickPrice')
        
        self.tws.connect()
    
    def __create_contract(self):
        self.contract = Contract()
        self.contract.m_symbol = self.symbol
        self.contract.m_secType= self.sec_type
        self.contract.m_exchange = self.exchange
        self.contract.m_expiry = self.expiry
        self.contract.m_currency = self.currency
    
    def __check_server_time(self):
        server_time = datetime.datetime.now()
    
        if self.last_time == None:
            self.last_time = server_time
    
        target_time = self.last_time + datetime.timedelta(minutes=1)
    
        if server_time.minute == (target_time - datetime.timedelta(minutes = 1)).minute and server_time.second==58 and not self.early_check:
            if self.debug:
                print '58s interval'
                print server_time.strftime('%Y-%m-%d %H:%M:%S')
            
            self.early_check=True
#             init_strategy()
        elif server_time.minute == target_time.minute and server_time.second == 0:
            if self.debug:
                print '00 interval'
                print server_time.strftime('%Y-%m-%d %H:%M:%S')
            
            self.last_time = server_time
            self.early_check = False
            
            if self.early_buy:
                self.early_buy = False
                return
            
#             init_strategy()

    def init_strategt(self):
        self.feed = ib_data_feed.IbDataFeed(60)
        self.feed_high = ib_data_feed.IbDataFeed(60)
        self.feed_low = ib_data_feed.IbDataFeed(60)
        self.feed_late = ib_data_feed.IbDataFeed(60)
        
        c = Contract()
        
        c.m_symbol = self.symbol
        c.m_secType= self.sec_type
        c.m_exchange = self.exchange
        c.m_expiry = self.exchange
        
        now = datetime.datetime.now()
        time_now = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        self.tws.reqHistoricalData(self.tracker_id, c, time_now, "1 D", "1 min", "TRADES", 0, 1)
    
    def prepare(self):
        logging.basicConfig(level = logging.INFO, filename = self.current_stat + '_' + self.symbol + '_log.txt')
        
        self.__load_param()
        self.__connect_tws()
        self.__create_contract()
    
    def run(self):
        self.main_loop()
        
    def main_loop():
        self.tws.reqIds(self.order_id)
    
        while 1:
            self.__check_server_time()
            time.sleep(self.main_loop_interval)