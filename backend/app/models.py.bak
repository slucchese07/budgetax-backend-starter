from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Numeric, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base
from datetime import datetime

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    institution: Mapped[str | None] = mapped_column(String(100))
    owner_key: Mapped[str] = mapped_column(String(128), index=True)  # simple multi-tenant via API key

    transactions = relationship("Transaction", back_populates="account")

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    ato_label: Mapped[str | None] = mapped_column(String(120))  # AU tax label mapping
    deductible_default: Mapped[bool] = mapped_column(Boolean, default=False)

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    posted_at: Mapped[datetime] = mapped_column(DateTime, index=True, default=datetime.utcnow)
    description: Mapped[str] = mapped_column(Text)
    amount: Mapped[float] = mapped_column(Numeric(12,2))  # negative = debit/expense
    currency: Mapped[str] = mapped_column(String(3), default="AUD")
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    deductible: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_key: Mapped[str] = mapped_column(String(128), index=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category")

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    purchase_date = mapped_column(Date)
    cost: Mapped[float] = mapped_column(Numeric(12,2))
    method: Mapped[str] = mapped_column(String(10))  # 'PC' or 'DV'
    effective_life_years: Mapped[int] = mapped_column(Integer)
    salvage_value: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    owner_key: Mapped[str] = mapped_column(String(128), index=True)

class DepreciationEntry(Base):
    __tablename__ = "depreciation_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"))
    fy_label: Mapped[str] = mapped_column(String(9), index=True)  # e.g., '2024-25'
    opening_value: Mapped[float] = mapped_column(Numeric(12,2))
    depreciation: Mapped[float] = mapped_column(Numeric(12,2))
    closing_value: Mapped[float] = mapped_column(Numeric(12,2))

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    issued_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="unpaid")  # unpaid, paid, overdue

# ----------------- Liabilities -----------------
class Liability(Base):
    __tablename__ = "liabilities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=True)
    length_of_loan = Column(String, nullable=True)

class Liability(Base):
    __tablename__ = "liabilities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=True)
    length_of_loan = Column(String, nullable=True)
