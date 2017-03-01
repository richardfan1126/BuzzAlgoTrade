import datetime, time

from ib.opt import Connection
from ib.ext.Contract import Contract

from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.feed import ib_data_feed 

class IBTradeStrategy():
    feed = None
    feed_high = None
    feed_low = None
    feed_late = None
    
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
            self.symbol = kwargs['sec_type']
        
        if 'exchange' in kwargs:
            self.symbol = kwargs['exchange']
        
        if 'expiry' in kwargs:
            self.symbol = kwargs['expiry']
        
        if 'currency' in kwargs:
            self.symbol = kwargs['currency']
        
        if 'param_set_name' in kwargs:
            self.symbol = kwargs['param_set_name']
        
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
        
    def prepare(self):
        logging.basicConfig(level = logging.INFO, filename = self.current_stat + '_' + SYMBOL + '_log.txt')
        
        self.tws.register(self.historical_data_handler, 'HistoricalData')
        self.tws.register(self.next_valid_id_handler, 'NextValidId')
        self.tws.register(self.order_status_handler, 'OrderStatus')
        self.tws.register(self.tick_price_handler, 'TickPrice')
        
        self.tws.connect()
        
        self.contract = Contract()
        self.contract.m_symbol = self.symbol
        self.contract.m_secType= self.sec_type
        self.contract.m_exchange = self.exchange
        self.contract.m_expiry = self.expiry
        self.contract.m_currency = self.currency
        
    def run(self):
        self.main_loop()
        
    def main_loop():
        self.tws.reqIds(self.order_id)
    
        while 1:
            self.extract_time_handler()
            time.sleep(0.2)