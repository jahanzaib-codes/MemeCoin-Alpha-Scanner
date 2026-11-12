"""
Pydantic schemas for on-chain tokens, smart-money wallets, and honeypot audits.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ChainNetwork(str, Enum):
    SOLANA = "SOLANA"
    BASE = "BASE"
    ETHEREUM = "ETHEREUM"
    BSC = "BSC"


class RiskVerdict(str, Enum):
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    HIGH_RISK = "HIGH_RISK"
    HONEYPOT = "HONEYPOT"
    RUG_PULL = "RUG_PULL"


class TokenSecurityAudit(BaseModel):
    mint_authority_revoked: bool
    freeze_authority_revoked: bool
    lp_burned_or_locked_pct: float
    top_10_holders_pct: float
    dev_wallet_holding_pct: float
    buy_tax_pct: float
    sell_tax_pct: float
    is_honeypot: bool
    is_bundle_launch: bool
    risk_score: float  # 0.0 (Clean/Safe) to 100.0 (Deadly/Honeypot)
    verdict: RiskVerdict
    red_flags: List[str] = Field(default_factory=list)


class SmartMoneyWallet(BaseModel):
    address: str
    label: str
    historical_win_rate_pct: float
    realized_pnl_usd: float
    total_trades_count: int
    chain: ChainNetwork


class TokenLaunchEvent(BaseModel):
    mint: str
    name: str
    symbol: str
    chain: ChainNetwork
    dex: str  # Raydium, Pump.fun, Uniswap V3, Aerodrome
    initial_liquidity_usd: float
    market_cap_usd: float
    price_usd: float
    volume_5m_usd: float
    holder_count: int
    smart_money_inflows_usd: float
    smart_money_buyers: List[str] = Field(default_factory=list)
    security_audit: TokenSecurityAudit
    alpha_score: float  # Composite metric from 0.0 to 100.0
    timestamp: str
