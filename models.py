from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class MutualFund(Base):
    __tablename__ = "mutual_funds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class SectorAllocation(Base):
    __tablename__ = "sector_allocations"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey('mutual_funds.id'))
    sector = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)

class StockAllocation(Base):
    __tablename__ = "stock_allocations"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey('mutual_funds.id'))
    stock = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)

class MarketCapAllocation(Base):
    __tablename__ = "market_cap_allocations"
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey('mutual_funds.id'))
    cap_type = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)

class Investment(Base):
    __tablename__ = "investments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    fund_id = Column(Integer, ForeignKey('mutual_funds.id'))
    amount = Column(Float, nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    isn = Column(String, nullable=False)
    nav_at_investment = Column(Float, nullable=False)
    returns_since_investment = Column(Float, nullable=False)
