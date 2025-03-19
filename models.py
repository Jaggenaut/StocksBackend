from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship


# Mutual Fund Table
class MutualFund(Base):
    __tablename__ = "mutual_funds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# Sector Table
class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    sector_allocations = relationship("SectorAllocation", back_populates="sector", cascade="all, delete-orphan")
    stocks = relationship("SectorStock", back_populates="sector", cascade="all, delete-orphan")

# Stock Table
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    stock_allocations = relationship("StockAllocation", back_populates="stock", cascade="all, delete-orphan")
    sectors = relationship("SectorStock", back_populates="stock", cascade="all, delete-orphan")

# Many-to-Many Relationship Between Stocks and Sectors
class SectorStock(Base):
    __tablename__ = "sector_stocks"

    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id", ondelete="CASCADE"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)

    sector = relationship("Sector", back_populates="stocks")
    stock = relationship("Stock", back_populates="sectors")

    __table_args__ = (UniqueConstraint("sector_id", "stock_id", name="uq_sector_stock"),)

# Updated Sector Allocation Table (Now References Sector by ID)
class SectorAllocation(Base):
    __tablename__ = "sector_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=False)
    percentage = Column(Float, nullable=False)

    sector = relationship("Sector", back_populates="sector_allocations")

# Updated Stock Allocation Table (Now References Stock by ID)
class StockAllocation(Base):
    __tablename__ = "stock_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    percentage = Column(Float, nullable=False)

    stock = relationship("Stock", back_populates="stock_allocations")

# Market Cap Allocation Table
class MarketCapAllocation(Base):
    __tablename__ = "market_cap_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    cap_type = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)

# Investment Table
class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"))
    amount = Column(Float, nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    isn = Column(String, nullable=False)
    nav_at_investment = Column(Float, nullable=False)
    returns_since_investment = Column(Float, nullable=False)
