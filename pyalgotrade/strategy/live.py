import datetime, time, sys

from ib.opt import Connection
from ib.ext.Contract import Contract

from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.feed import ib_data_feed 
from pyalgotrade.models.initParams import InitParam

class IBTradeStrategy():
    feed = None
    feed_high = None
    feed_low = None
    feed_late = None
    
    initParam = None
    db_username = None
    db_password = None
    db_host = None
    db_database = None
    
    contract = None
    
    order_id = 1
    
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
            return
    
        if msg.date[:8] != "finished":
            date = utc.strftime("%Y-%m-%d %H:%M:%S")
            if utc.time()!=server_time.time():
                self.feed.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
        else:
            self.feed.finishAddBar(self.instrument_name)
            if self.feed.get_count() >= self.min_feed_required:
                self.run()
    
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
    
    def prepare(self):
        logging.basicConfig(level = logging.INFO, filename = self.current_stat + '_' + SYMBOL + '_log.txt')
        
        self.__load_param()
        self.__connect_tws()
        self.__create_contract()
        
    def run(self):
        self.main_loop()
        
    def main_loop():
        self.tws.reqIds(self.order_id)
    
        while 1:
            self.extract_time_handler()
            time.sleep(0.2)