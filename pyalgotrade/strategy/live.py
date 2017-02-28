from ib.opt import Connection

class IBTradeStrategy():
    min_feed_required = 54
    instrument_name = 'hsi'
    
    def __init__(self):
        self.tws = Connection.create(port=7496, clientId=CLIENT_ID)
    
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
        self.tws.register(next_valid_id_handler, 'NextValidId')
        self.tws.register(order_status_handler, 'OrderStatus')
        self.tws.register(tick_price_handler, 'TickPrice')
        
        self.tws.connect()