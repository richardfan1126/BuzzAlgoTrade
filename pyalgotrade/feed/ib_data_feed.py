from pyalgotrade.utils import dt

from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar

import datetime

class IbRowParser(csvfeed.GenericRowParser):
    def __init__(self, dateTimeFormat, dailyBarTime, frequency, timezone, barClass=bar.BasicBar):
        self.__dateTimeFormat = dateTimeFormat
        self.__dailyBarTime = dailyBarTime
        self.__frequency = frequency
        self.__timezone = timezone
        self.__haveAdjClose = False
        self.__barClass = barClass

    def parseBar(self, dateTime, open_, close, low, high, volumne):
        try:
            dateTime = self._parseDate(dateTime)
        except ValueError:
            return None

        adjClose = None

        return self.__barClass(
            dateTime, open_, high, low, close, volumne, adjClose, self.__frequency
        )

    def _parseDate(self, dateString):
        ret = datetime.datetime.strptime(dateString, self.__dateTimeFormat)

        if self.__dailyBarTime is not None:
            ret = datetime.datetime.combine(ret, self.__dailyBarTime)
        # Localize the datetime if a timezone was given.
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret


class IbDataFeed(csvfeed.GenericBarFeed):
    def __init__(self, frequency, timezone=None, maxLen=None):
        super(IbDataFeed, self).__init__(frequency, timezone, maxLen)
        self.loadedBars = []

    def addBar(self, dateTime, open_, close, low, high, volumne):
        rowParser = IbRowParser("%Y-%m-%d %H:%M:%S", None, self.getFrequency(), None)
        bar_ = rowParser.parseBar(dateTime, open_, close, low, high, volumne)

        if bar_ is not None:
            self.loadedBars.append(bar_)
    
    def removeLastBar(self, instrument):
        del self.loadedBars[-1]
        self.finishAddBar(instrument)

    def finishAddBar(self, instrument):
        self.reset()
        self.addBarsFromSequence(instrument, self.loadedBars)
        
    def get_count(self):
        return len(self.loadedBars)

