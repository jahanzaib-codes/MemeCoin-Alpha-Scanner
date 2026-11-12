"""
Real-time Token Stream Scanner.
Aggregates new liquidity pool creations, runs instant security audits, and computes Alpha Scores.
"""

from datetime import datetime, timezone
from typing import List, Optional
from src.models.token_models import (
    ChainNetwork,
    RiskVerdict,
    TokenLaunchEvent,
    TokenSecurityAudit,
)
from src.security.honeypot_filter import HoneypotFilter
from src.tracker.smart_money import SmartMoneyTracker


# Simulated live on-chain token feed
LIVE_TOKEN_FEED = [
    {
        "mint": "7pB8Q9gRtY4kP9jK1mZ8vL3wQ2eR4tY6uI8oP0aSDFG",
        "name": "Pepe Quantum AI",
        "symbol": "PEPEAI",
        "chain": ChainNetwork.SOLANA,
        "dex": "Pump.fun",
        "initial_liquidity_usd": 12500.0,
        "market_cap_usd": 68000.0,
        "price_usd": 0.000068,
        "volume_5m_usd": 42000.0,
        "holder_count": 218,
        "buyers": ["7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"],
        "audit_params": {
            "mint_auth_revoked": True,
            "freeze_auth_revoked": True,
            "lp_burned_or_locked_pct": 100.0,
            "top_10_holders_pct": 0.18,
            "dev_wallet_holding_pct": 0.03,
            "buy_tax_pct": 0.0,
            "sell_tax_pct": 0.0,
            "is_bundle_launch": True,
        },
    },
    {
        "mint": "9aB8C7dE6fG5hI4jK3lM2nO1pQ0rS9tU8vW7xY6zABC",
        "name": "Solana Velocity Alpha",
        "symbol": "SVEL",
        "chain": ChainNetwork.SOLANA,
        "dex": "Raydium CPMM",
        "initial_liquidity_usd": 28000.0,
        "market_cap_usd": 145000.0,
        "price_usd": 0.000145,
        "volume_5m_usd": 95000.0,
        "holder_count": 482,
        "buyers": [
            "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
            "4ND1mBQtrMJWY7kG2rZ5t2eD61xT8g1U8N1p4Y9R8U9",
        ],
        "audit_params": {
            "mint_auth_revoked": True,
            "freeze_auth_revoked": True,
            "lp_burned_or_locked_pct": 100.0,
            "top_10_holders_pct": 0.24,
            "dev_wallet_holding_pct": 0.04,
            "buy_tax_pct": 0.0,
            "sell_tax_pct": 0.0,
            "is_bundle_launch": False,
        },
    },
    {
        "mint": "0x4b8a2c1d9f8e7b6a5c4d3e2f1a0b9c8d7e6f5a4b",
        "name": "Based Shiba Bot",
        "symbol": "BSHIB",
        "chain": ChainNetwork.BASE,
        "dex": "Aerodrome",
        "initial_liquidity_usd": 18000.0,
        "market_cap_usd": 85000.0,
        "price_usd": 0.000085,
        "volume_5m_usd": 38000.0,
        "holder_count": 312,
        "buyers": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
        "audit_params": {
            "mint_auth_revoked": True,
            "freeze_auth_revoked": True,
            "lp_burned_or_locked_pct": 100.0,
            "top_10_holders_pct": 0.28,
            "dev_wallet_holding_pct": 0.05,
            "buy_tax_pct": 0.0,
            "sell_tax_pct": 0.0,
            "is_bundle_launch": False,
        },
    },
    {
        "mint": "ScamTokenTrapDangerousDoNotBuy1234567890123",
        "name": "Super Moon Doge 1000x",
        "symbol": "SMDOGE",
        "chain": ChainNetwork.SOLANA,
        "dex": "Pump.fun",
        "initial_liquidity_usd": 4000.0,
        "market_cap_usd": 12000.0,
        "price_usd": 0.000012,
        "volume_5m_usd": 14000.0,
        "holder_count": 35,
        "buyers": [],
        "audit_params": {
            "mint_auth_revoked": False,  # Mint authority active!
            "freeze_auth_revoked": False,  # Freeze authority active!
            "lp_burned_or_locked_pct": 20.0,  # Unlocked LP!
            "top_10_holders_pct": 0.75,
            "dev_wallet_holding_pct": 0.35,  # Dev has 35%!
            "buy_tax_pct": 0.05,
            "sell_tax_pct": 0.85,  # 85% sell tax honeypot!
            "is_bundle_launch": True,
        },
    },
]


class TokenStreamScanner:
    def __init__(self):
        self.security_filter = HoneypotFilter()
        self.smart_tracker = SmartMoneyTracker()

    def calculate_alpha_score(
        self,
        audit: TokenSecurityAudit,
        smart_buyers_count: int,
        volume_5m: float,
        initial_liquidity: float,
    ) -> float:
        # If marked as Honeypot or Rug Pull, Alpha Score is strictly 0.0
        if audit.verdict in [RiskVerdict.HONEYPOT, RiskVerdict.RUG_PULL, RiskVerdict.HIGH_RISK]:
            return 0.0

        # Base security score (max 40 pts)
        security_pts = max(0.0, 40.0 - (audit.risk_score * 0.4))

        # Smart money confirmations (max 35 pts)
        smart_pts = min(35.0, smart_buyers_count * 17.5)

        # Liquidity & Volume health (max 25 pts)
        liq_pts = min(15.0, (initial_liquidity / 20000.0) * 15.0)
        vol_pts = min(10.0, (volume_5m / 50000.0) * 10.0)

        total = round(security_pts + smart_pts + liq_pts + vol_pts, 1)
        return min(100.0, max(0.0, total))

    def scan_new_launches(self, filter_safe_only: bool = False) -> List[TokenLaunchEvent]:
        events: List[TokenLaunchEvent] = []

        for item in LIVE_TOKEN_FEED:
            audit = self.security_filter.audit_token(
                mint=item["mint"],
                chain=item["chain"],
                **item["audit_params"],
            )

            if filter_safe_only and audit.verdict != RiskVerdict.SAFE:
                continue

            smart_buyers = self.smart_tracker.identify_buyers(item["buyers"])
            smart_inflows = self.smart_tracker.calculate_smart_money_inflow(smart_buyers, item["volume_5m_usd"])
            alpha = self.calculate_alpha_score(
                audit=audit,
                smart_buyers_count=len(smart_buyers),
                volume_5m=item["volume_5m_usd"],
                initial_liquidity=item["initial_liquidity_usd"],
            )

            events.append(
                TokenLaunchEvent(
                    mint=item["mint"],
                    name=item["name"],
                    symbol=item["symbol"],
                    chain=item["chain"],
                    dex=item["dex"],
                    initial_liquidity_usd=item["initial_liquidity_usd"],
                    market_cap_usd=item["market_cap_usd"],
                    price_usd=item["price_usd"],
                    volume_5m_usd=item["volume_5m_usd"],
                    holder_count=item["holder_count"],
                    smart_money_inflows_usd=smart_inflows,
                    smart_money_buyers=[b.label for b in smart_buyers],
                    security_audit=audit,
                    alpha_score=alpha,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                )
            )

        events.sort(key=lambda x: x.alpha_score, reverse=True)
        return events
