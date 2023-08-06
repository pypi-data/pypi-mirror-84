import collections
import logging
import requests

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import fredapi
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

Event = collections.namedtuple('Event', ['name', 'start_date', 'end_date'])
dotcom = Event(
    name='Dotcom Crash', 
    start_date=pd.Timestamp(year=2000, month=3, day=24), 
    end_date=pd.Timestamp(year=2002, month=10, day=9)
)
gfc = Event(
    name='GFC', 
    start_date=pd.Timestamp(year=2007, month=10, day=9), 
    end_date=pd.Timestamp(year=2009, month=3, day=9)
)
euro_debt = Event(
    name='Euro Crisis', 
    start_date=pd.Timestamp(year=2011, month=2, day=8), 
    end_date=pd.Timestamp(year=2011, month=9, day=22)
)
oil_supply_glut_2015 = Event(
    name='Oil Crisis', 
    start_date=pd.Timestamp(year=2015, month=5, day=21), 
    end_date=pd.Timestamp(year=2016, month=2, day=11)
) 
covid = Event(
    name='COVID-19', 
    start_date=pd.Timestamp(year=2019, month=12, day=31), 
    end_date=pd.Timestamp.now()
)
opec_russia_disagreement = Event(
    name='OPEC-Russia Disagreement', 
    start_date=pd.Timestamp(year=2020, month=3, day=9), 
    end_date=pd.Timestamp(year=2020, month=4, day=9)
)

def get_equity_data_from_alphavantage(api_key, tickers, fields='adjusted_close', names=None):
    if isinstance(tickers, str):
        tickers = [tickers]

    if isinstance(names, str):
        names = [names]
    
    if isinstance(fields, str):
        fields = fields[fields]

    ts = TimeSeries(key=api_key, output_format='pandas')

    metadata = {field: [] for field in fields}

    for ticker_idx, ticker in enumerate(tickers):
        logger.info('Getting %s data' % ticker)

        df = ts.get_daily_adjusted(symbol=ticker, outputsize='full')[0]
        df.columns = [col[3:].replace(' ', '_') for col in df.columns]
        df = df.iloc[::-1]
        
        for field in fields:
            try:
                if names is None:
                    metadata[field].append(df[field].to_frame(ticker))
                else:
                    metadata[field].append(df[field].to_frame(names[ticker_idx]))
            except KeyError:
                raise KeyError('There is no field called `%s` in equity data from Alphavantage.' % field)

    if len(metadata.keys()) == 1:
        return metadata[list(metadata.keys())[0]]

    return metadata

def get_fx_data_from_alphavantage(api_key, from_tickers, to_tickers, fields='close'):
    if isinstance(from_tickers, str):
        from_tickers = [from_tickers]
    
    if isinstance(to_tickers, str):
        to_tickers = [to_tickers]

    if isinstance(fields, str):
        fields = fields[fields]    

    fx = ForeignExchange(key=api_key, output_format='pandas')

    metadata = {field: [] for field in fields}

    for from_ticker, to_ticker in zip(from_tickers, to_tickers):
        logger.info('Getting %s%s data' % (from_ticker, to_ticker))

        df = fx.get_currency_exchange_daily(from_symbol=from_symbol, to_symbol=to_symbol, outputsize='full')[0]
        df.columns = [col[3:].replace(' ', '_') for col in df.columns]
        df = df.iloc[::-1]
        
        for field in fields:
            try:
                metadata[field].append(df[field].to_frame(from_ticker + to_ticker))
            except KeyError:
                raise KeyError('There is no field called `%s` in FX data from Alphavantage.' % field)

    if len(metadata.keys()) == 1:
        return metadata[list(metadata.keys())[0]]

    return metadata

class BancoDeMexico:
    """This class allows us to extract data from Banco de Mexico's API. To see what series are available,
    please see `here <https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries>`."""

    def __init__(self, token):
        self.TOKEN = token
        self.MAX_TICKERS = 20
        self.METADATA_URL = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/%s'
        self.TIMESERIES_URL = self.METADATA_URL + '/datos'

        self.SPANISH_TO_ENGLISH_NAMES = {
            'titulo': 'title',
            'idSerie': 'ticker',
            'datos': 'datas',
            'dato': 'data',
            'fecha': 'date',
            'fechaInicio': 'start_date',
            'fechaFin': 'end_date',
            'periodicidad': 'frequency',
            'unidad': 'unit',
            'cifra': 'figure'
        }

    def _translate_data_type_names(self, spanish_name):
        try:
            return self.SPANISH_TO_ENGLISH_NAMES[spanish_name]
        except KeyError:
            return spanish_name

    def get_metadata(self, tickers):
        if len(tickers) > self.MAX_TICKERS:
            raise ValueError('Maximum of %d tickers allowed.' % self.MAX_TICKERS)

        if isinstance(tickers, str):
            tickers = [tickers]

        tickers_str = ','.join(tickers)
        url = self.METADATA_URL % tickers_str
        params = {
            'token': self.TOKEN,
            'locale': 'en'
        }

        response = requests.get(url, params=params)
        assert response.status_code == 200

        all_series = response.json()['bmx']['series']
        metadata = pd.concat(
            [
                pd.DataFrame.from_dict(series, orient='index').T.set_index('idSerie') for series in all_series
            ]
        ).rename_axis(None)
        metadata.columns = [self._translate_data_type_names(spanish_name) for spanish_name in metadata.columns]

        return metadata
    
    def get(self, tickers):
        if len(tickers) > self.MAX_TICKERS:
            raise ValueError('Maximum of %d tickers allowed.' % self.MAX_TICKERS)

        if isinstance(tickers, str):
            tickers = [tickers]

        tickers_str = ','.join(tickers)
        url = self.TIMESERIES_URL % tickers_str
        params = {
            'token': self.TOKEN,
            'locale': 'en'
        }    

        response = requests.get(url, params=params)
        assert response.status_code == 200

        all_series = response.json()['bmx']['series']

        def dict_to_df(dictionary):
            df = pd.DataFrame.from_records(dictionary['datos']).set_index('fecha')
            df.index = [pd.to_datetime(date, format='%d/%m/%Y') for date in df.index]
            df.columns = [dictionary['idSerie']]
            df[dictionary['idSerie']] = [float(val.replace(',', '')) for val in df[dictionary['idSerie']]]
            return df

        ts = pd.concat(
            [dict_to_df(series) for series in all_series], axis=1
        ).rename_axis(None)

        return ts
