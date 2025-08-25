from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List

# Shared
class Message(BaseModel):
    message: str

# Accounts
class AccountIn(BaseModel):
    name: str
    institution: Optional[str] = None

class AccountOut(AccountIn):
    id: int

# Categories
class CategoryIn(BaseModel):
    name: str
    ato_label: Optional[str] = None
    deductible_default: bool = False

class CategoryOut(CategoryIn):
    id: int

# Transactions
class TransactionIn(BaseModel):
    account_id: int
    posted_at: Optional[datetime] = None
    description: str
    amount: float
    currency: str = "AUD"
    category_id: Optional[int] = None
    deductible: Optional[bool] = None

class TransactionOut(TransactionIn):
    id: int

class TransactionImport(BaseModel):
    items: List[TransactionIn]

class IncomeIn(BaseModel):
    description: str
    amount: float  # positive value for income
    posted_at: Optional[datetime] = None
    account_id: Optional[int] = None
    currency: str = "AUD"
class ExpenseIn(BaseModel):
    description: str
    amount: float                 # positive number you spent, e.g., 45.00
    posted_at: Optional[datetime] = None
    account_id: Optional[int] = None
    currency: str = "AUD"
    category_name: Optional[str] = "General"
    deductible: bool = True       # default: expenses are deductible unless you say otherwise

# Assets
class AssetIn(BaseModel):
    name: str
    purchase_date: date
    cost: float
    method: str = Field(pattern="^(PC|DV)$")
    effective_life_years: int
    salvage_value: float = 0.0

class AssetOut(AssetIn):
    id: int

class InvoiceIn(BaseModel):
    client_name: str
    description: str
    amount: float
    issued_date: date
    due_date: date
    status: str = "unpaid"

class InvoiceOut(InvoiceIn):
    id: int

class DepreciationEntryOut(BaseModel):
    id: int
    asset_id: int
    fy_label: str
    opening_value: float
    depreciation: float
    closing_value: float

# Summaries
class TaxSummaryRow(BaseModel):
    ato_label: str
    total: float

class TaxSummaryOut(BaseModel):
    fy_label: str
    currency: str = "AUD"
    totals: list[TaxSummaryRow]
