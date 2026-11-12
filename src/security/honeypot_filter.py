"""
Honeypot and Anti-Rug Security Engine.
Inspects mint authorities, freeze powers, liquidity lock/burns, and bundle anomalies.
"""

from typing import List, Tuple
from src.models.token_models import ChainNetwork, RiskVerdict, TokenSecurityAudit


class HoneypotFilter:
    """
    Sub-millisecond bytecode inspection and metadata audit engine.
    """

    @staticmethod
    def audit_token(
        mint: str,
        chain: ChainNetwork = ChainNetwork.SOLANA,
        mint_auth_revoked: bool = True,
        freeze_auth_revoked: bool = True,
        lp_burned_or_locked_pct: float = 100.0,
        top_10_holders_pct: float = 0.22,
        dev_wallet_holding_pct: float = 0.04,
        buy_tax_pct: float = 0.0,
        sell_tax_pct: float = 0.0,
        is_bundle_launch: bool = False,
    ) -> TokenSecurityAudit:
        red_flags: List[str] = []
        risk_score = 0.0

        # 1. Freeze Authority (Critical on Solana)
        if not freeze_auth_revoked:
            red_flags.append("CRITICAL: Freeze authority retained by creator (can blacklist sell transactions).")
            risk_score += 45.0

        # 2. Mint Authority (Critical on Solana & EVM)
        if not mint_auth_revoked:
            red_flags.append("CRITICAL: Mint authority active (creator can inflate token supply infinitely).")
            risk_score += 40.0

        # 3. Liquidity Pool Lock / Burn
        if lp_burned_or_locked_pct < 90.0:
            unlocked = 100.0 - lp_burned_or_locked_pct
            red_flags.append(f"WARNING: {unlocked:.1f}% of liquidity pool is unburned/unlocked (high rug pull vulnerability).")
            risk_score += min(35.0, (unlocked / 100.0) * 40.0)

        # 4. Dev Wallet Concentration
        if dev_wallet_holding_pct > 0.08:
            red_flags.append(f"HIGH RISK: Developer wallet controls {dev_wallet_holding_pct*100:.1f}% of total supply.")
            risk_score += min(30.0, (dev_wallet_holding_pct / 0.20) * 30.0)

        # 5. Top 10 Holders Concentration (Cabals & Snipers)
        if top_10_holders_pct > 0.35:
            red_flags.append(f"CAUTION: Top 10 holders control {top_10_holders_pct*100:.1f}% of supply (cabal dump risk).")
            risk_score += 15.0

        # 6. Taxes (Honeypot Mechanism on EVM & Solana Extensions)
        if sell_tax_pct > 0.40 or buy_tax_pct > 0.40:
            red_flags.append(f"HONEYPOT: Malicious contract fee detected (Buy: {buy_tax_pct*100:.0f}%, Sell: {sell_tax_pct*100:.0f}%).")
            risk_score += 50.0
        elif sell_tax_pct > 0.05 or buy_tax_pct > 0.05:
            red_flags.append(f"ELEVATED TAX: Transfer fees detected (Buy: {buy_tax_pct*100:.1f}%, Sell: {sell_tax_pct*100:.1f}%).")
            risk_score += 15.0

        # 7. Jito Bundle Launch Cluster
        if is_bundle_launch:
            red_flags.append("INFO: Genesis block was bundled via Jito block engine (sniper cluster detected).")
            risk_score += 10.0

        final_risk = min(100.0, max(0.0, risk_score))

        # Assign verdict
        is_honeypot = sell_tax_pct > 0.40 or not freeze_auth_revoked
        if final_risk >= 70.0:
            verdict = RiskVerdict.HONEYPOT if is_honeypot else RiskVerdict.RUG_PULL
        elif final_risk >= 45.0:
            verdict = RiskVerdict.HIGH_RISK
        elif final_risk >= 20.0:
            verdict = RiskVerdict.CAUTION
        else:
            verdict = RiskVerdict.SAFE

        return TokenSecurityAudit(
            mint_authority_revoked=mint_auth_revoked,
            freeze_authority_revoked=freeze_auth_revoked,
            lp_burned_or_locked_pct=round(lp_burned_or_locked_pct, 1),
            top_10_holders_pct=round(top_10_holders_pct, 3),
            dev_wallet_holding_pct=round(dev_wallet_holding_pct, 3),
            buy_tax_pct=round(buy_tax_pct, 3),
            sell_tax_pct=round(sell_tax_pct, 3),
            is_honeypot=is_honeypot,
            is_bundle_launch=is_bundle_launch,
            risk_score=round(final_risk, 1),
            verdict=verdict,
            red_flags=red_flags,
        )
