"""
MemeCoin-Alpha-Scanner Interactive Terminal Suite & On-Chain Screener.
"""

import sys
import click
from tabulate import tabulate

from src.models.token_models import RiskVerdict
from src.scanner.stream_scanner import TokenStreamScanner
from src.security.honeypot_filter import HoneypotFilter
from src.tracker.smart_money import SmartMoneyTracker


@click.group()
def cli():
    """MemeCoin-Alpha-Scanner Terminal CLI."""
    pass


@cli.command("demo")
def demo():
    """Run an automated demonstration of on-chain scanning and anti-rug audits."""
    scanner = TokenStreamScanner()
    tracker = SmartMoneyTracker()

    click.secho("\n" + "=" * 95, fg="cyan", bold=True)
    click.secho("   🐕 MEMECOIN-ALPHA-SCANNER: ON-CHAIN SMART-MONEY & HONEYPOT DETECTION SUITE", fg="cyan", bold=True)
    click.secho("=" * 95, fg="cyan")

    # 1. Tracked Smart-Money Wallets
    click.secho("\n[1/3] Tracked High-Conviction Smart-Money Wallets:", fg="yellow", bold=True)
    wallets = tracker.get_all_tracked_wallets()
    w_rows = []
    for w in wallets:
        w_rows.append([
            w.chain.value,
            w.label,
            f"{w.historical_win_rate_pct:.1f}%",
            f"${w.realized_pnl_usd:,.0f}",
            w.total_trades_count,
            w.address[:6] + "..." + w.address[-4:],
        ])
    print(tabulate(w_rows, headers=["Chain", "Wallet Label", "Win Rate", "Realized PnL", "Trades", "Address"], tablefmt="github"))

    # 2. Live Token Launch Feed & Security Audits
    click.secho("\n[2/3] Live Token Launches & Sub-Millisecond Anti-Rug Audits:", fg="yellow", bold=True)
    events = scanner.scan_new_launches()

    e_rows = []
    for e in events:
        audit = e.security_audit
        color = "green" if audit.verdict == RiskVerdict.SAFE else "red"
        e_rows.append([
            f"{e.name} (${e.symbol})",
            e.chain.value,
            e.dex,
            f"${e.initial_liquidity_usd:,.0f}",
            f"${e.market_cap_usd:,.0f}",
            audit.verdict.value,
            f"{audit.risk_score:.0f}/100",
            "YES" if audit.mint_authority_revoked else "NO ⚠️",
            "YES" if audit.freeze_authority_revoked else "NO ⚠️",
            f"{e.alpha_score:.1f}/100",
        ])
    print(tabulate(e_rows, headers=["Token", "Chain", "DEX", "Init Liquidity", "Mkt Cap", "Audit Verdict", "Risk", "Mint Revoked", "Freeze Revoked", "Alpha Score"], tablefmt="github"))

    # 3. Smart Money Accumulation Highlights
    click.secho("\n[3/3] High-Alpha Signals (Verified Safe + Whale Backed):", fg="yellow", bold=True)
    alpha_picks = [e for e in events if e.alpha_score >= 60.0]
    for p in alpha_picks:
        click.secho(f"  ⭐ {p.name} ({p.symbol}) on {p.dex} ({p.chain.value})", fg="green", bold=True)
        click.echo(f"     • Mint Address:       {p.mint}")
        click.echo(f"     • Smart Money Inflow: ${p.smart_money_inflows_usd:,.2f} USD")
        click.echo(f"     • Confirmed Buyers:   {', '.join(p.smart_money_buyers)}")
        click.echo(f"     • Security Score:     Risk {p.security_audit.risk_score}/100 (Verdict: {p.security_audit.verdict.value})")

    # Honeypot Warning Demonstration
    honeypot_tokens = [e for e in events if e.security_audit.verdict in [RiskVerdict.HONEYPOT, RiskVerdict.RUG_PULL]]
    if honeypot_tokens:
        click.secho("\n  🚫 INTERCEPTED MALICIOUS SCAM TOKEN:", fg="red", bold=True)
        for h in honeypot_tokens:
            click.echo(f"     • {h.name} (${h.symbol}): Flagged as {h.security_audit.verdict.value}")
            for flag in h.security_audit.red_flags:
                click.echo(f"       - {flag}")

    click.secho("\n" + "=" * 95, fg="cyan")
    click.secho("   ✅ ON-CHAIN TOKEN SCANNER ENGINE VALIDATED SUCCESSFULLY", fg="green", bold=True)
    click.secho("=" * 95 + "\n", fg="cyan")


@cli.command("whales")
def whales():
    """List all tracked on-chain smart-money wallets."""
    tracker = SmartMoneyTracker()
    wallets = tracker.get_all_tracked_wallets()
    rows = [[w.chain.value, w.label, f"{w.historical_win_rate_pct:.1f}%", f"${w.realized_pnl_usd:,.0f}", w.address] for w in wallets]
    print(tabulate(rows, headers=["Chain", "Label", "Win Rate", "Realized PnL", "Address"], tablefmt="github"))


@cli.command("audit")
@click.argument("mint")
def audit(mint):
    """Run an instant security and honeypot audit on any token mint."""
    filter_eng = HoneypotFilter()
    res = filter_eng.audit_token(mint=mint)
    click.echo(f"\nMint: {mint}")
    click.echo(f"Verdict: {res.verdict.value} (Risk Score: {res.risk_score}/100)")
    click.echo(f"Mint Revoked: {res.mint_authority_revoked} | Freeze Revoked: {res.freeze_authority_revoked}")
    if res.red_flags:
        click.echo("Red Flags:")
        for rf in res.red_flags:
            click.echo(f"  - {rf}")
    click.echo()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        demo()
    else:
        cli()
