import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = db.create_engine('sqlite:///crypto_index.db')
Base = declarative_base()


class CryptoCurrencies(Base):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String)


class MarketData(Base):
    """
    The class houses the market data extracted from CoinMarketCap
    """

    __tablename__ = 'marketdata'

    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column('crypto', db.Integer, db.ForeignKey('currencies.id'))
    load_date = db.Column(db.DateTime)
    market_cap = db.Column(db.Integer)
    market_cap_percentage = db.Column(db.Float)
    trade_price = db.Column(db.Float)
    ranking = db.Column(db.Integer)


class CryptoRunningAverages(Base):
    """
    Quantifying the running averages for all the cryptocurrency indices that are being mapped into the ranking
    """
    __tablename__ = 'averages'

    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column('crypto', db.Integer, db.ForeignKey('currencies.id'))
    load_date = db.Column(db.DateTime)

    ewma_market_cap = db.Column(db.Float)
    ewma_market_cap_percentage = db.Column(db.Float)
    ewma_trade_price = db.Column(db.Float)
    ewma_volatility = db.Column(db.Float)

    ewma_ranking = db.Column(db.Integer)


class IndexRanking(Base):
    """
    Ranks the Index at the given point in time to determine what the percentage of the investment will be put into
    each currency
    """

    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column('crypto', db.Integer, db.ForeignKey('currencies.id'))
    load_date = db.Column(db.DateTime)
    index_ranking = db.column(db.Integer)
    index_percentage = db.column(db.Float)


class PurchaseHistory(Base):
    """
    Logs the purchase history of the cryptocurrencies to map them over time
    """

    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column('crypto', db.Integer, db.ForeignKey('currencies.id'))
    load_date = db.Column(db.DateTime)
    purchase_amt_usd = db.Column(db.Float)
    purchase_amt_crypto = db.Column(db.Float)


Base.metadata.create_all(engine)
