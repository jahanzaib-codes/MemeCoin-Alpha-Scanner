"""
Smart-Money Wallet Profiler.
Monitors high-conviction on-chain whales, profitable snipers, and insider wallets.
"""

from typing import Dict, List, Optional
from src.models.token_models import ChainNetwork, SmartMoneyWallet


CURATED_WALLETS = [
    SmartMoneyWallet(
        address="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
        label="Whale Sniper (Alpha Lead)",
        historical_win_rate_pct=78.5,
        realized_pnl_usd=1420000.0,
        total_trades_count=342,
        chain=ChainNetwork.SOLANA,
    ),
    SmartMoneyWallet(
        address="4ND1mBQtrMJWY7kG2rZ5t2eD61xT8g1U8N1p4Y9R8U9",
        label="Pump.fun Micro-Cap Insider",
        historical_win_rate_pct=84.2,
        realized_pnl_usd=890000.0,
        total_trades_count=215,
        chain=ChainNetwork.SOLANA,
    ),
    SmartMoneyWallet(
        address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        label="Vitalik / EVM Tier-1 Whale",
        historical_win_rate_pct=91.0,
        realized_pnl_usd=5600000.0,
        total_trades_count=180,
        chain=ChainNetwork.BASE,
    ),
    SmartMoneyWallet(
        address="9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
        label="Raydium Fast Arb / Mev Engine",
        historical_win_rate_pct=74.0,
        realized_pnl_usd=620000.0,
        total_trades_count=612,
        chain=ChainNetwork.SOLANA,
    ),
]


class SmartMoneyTracker:
    def __init__(self):
        self.wallets: Dict[str, SmartMoneyWallet] = {w.address: w for w in CURATED_WALLETS}

    def get_all_tracked_wallets(self) -> List[SmartMoneyWallet]:
        return list(self.wallets.values())

    def identify_buyers(self, buyer_addresses: List[str]) -> List[SmartMoneyWallet]:
        matches: List[SmartMoneyWallet] = []
        for addr in buyer_addresses:
            if addr in self.wallets:
                matches.append(self.wallets[addr])
        return matches

    def calculate_smart_money_inflow(self, smart_buyers: List[SmartMoneyWallet], total_volume: float) -> float:
        if not smart_buyers:
            return 0.0
        # Estimate smart money accumulation volume
        pct = min(0.40, len(smart_buyers) * 0.12)
        return round(total_volume * pct, 2)
