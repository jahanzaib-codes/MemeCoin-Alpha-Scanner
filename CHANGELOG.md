# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-12

### Added
- **Honeypot & Anti-Rug Engine**:
  - Solana SPL freeze authority verification.
  - Mint authority revocation auditing.
  - LP burn percentage threshold monitoring.
  - Dev wallet concentration and Top-10 holder cabal detection.
  - EVM fee analysis (asymmetric buy/sell tax honey-trap detection).
  - Jito block engine bundle identification.
- **Smart Money Tracking Engine**:
  - High-conviction wallet directory (historical win rate, realized PnL, trade volume).
  - Multi-wallet consensus scoring.
  - Real-time inflow volume aggregation.
- **Token Launch Stream Scanner**:
  - Multi-chain DEX ingestion (Solana Raydium CPMM, Pump.fun, Base Aerodrome).
  - Composite Alpha Scoring formula balancing security risk and whale momentum.
- **Developer Interfaces**:
  - Interactive Click CLI (`cli.py`) with rich tabular reporting.
  - Containerization via multi-stage `Dockerfile` and `docker-compose.yml`.
  - Automated dual-version matrix CI/CD via GitHub Actions.
