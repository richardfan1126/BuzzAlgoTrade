import datetime, time

from ib.opt import Connection
from pyalgotrade.strategy import BacktestingStrategy

from pyalgotrade.feed import ib_data_feed 

class IBTradeStrategy():
    feed = None
    feed_high = None
    feed_low = None
    feed_late = None
    
    order_id = 1
    
    feed_frequency = 60
    min_feed_required = 54
    instrument_name = 'hsi'
    
    def __init__(self):
        self.tws = Connection.create(port = 7496, clientId = CLIENT_ID)
        
        slef.feed = ib_data_feed.IbDataFeed(self.feed_frequency)
        slef.feed_high = ib_data_feed.IbDataFeed(self.feed_frequency)
        slef.feed_low = ib_data_feed.IbDataFeed(self.feed_frequency)
        slef.feed_late = ib_data_feed.IbDataFeed(self.feed_frequency)
    
    def historical_data_handler(self, msg):
        try:
            utc = datetime.datetime.strptime(msg.date, '%Y%m%d  %H:%M:%S')
        except ValueError:
            print 'price tick handler value error'
            return
    
        if msg.date[:8] != "finished":
            date = utc.strftime("%Y-%m-%d %H:%M:%S")
            if utc.time()!=server_time.time():
                feed.addBar(date, msg.open, msg.close, msg.low, msg.high, msg.volume)
        else:
            feed.finishAddBar(self.instrument_name)
            if feed.get_count() >= self.min_feed_required:
                self.run()
        
    def prepare(self):
        self.tws.register(self.historical_data_handler, 'HistoricalData')
        self.tws.register(self.next_valid_id_handler, 'NextValidId')
        self.tws.register(self.order_status_handler, 'OrderStatus')
        self.tws.register(self.tick_price_handler, 'TickPrice')
        
        self.tws.connect()
        
    def run(self):
        self.main_loop()
        
    def main_loop():
        self.tws.reqIds(self.order_id)
    
        while 1:
            # tws.reqCurrentTime()
            self.extract_time_handler()
            time.sleep(0.2)