# Contributing to MemeCoin Alpha Scanner

Thank you for your interest in contributing to the **MemeCoin Alpha Scanner** project. This project implements high-throughput on-chain memecoin screening, sub-millisecond honeypot audits, and smart-money wallet flow tracking for Solana and EVM (Base) ecosystems.

## Guidelines

1. **Code Standards**:
   - Write clean, type-annotated Python 3.10+ compliant code.
   - Use `pydantic` schemas for any data interchange models.
   - Maintain static analysis compliance: zero warnings under `flake8` (`E9, F63, F7, F82, F824`).

2. **Commit Conventions**:
   Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
   - `feat(...)`: New features (e.g. new DEX adapters, token filter logic)
   - `fix(...)`: Bug fixes
   - `docs(...)`: Documentation updates
   - `infra(...)`: Docker, CI/CD, or deployment configurations

3. **Pull Request Workflow**:
   - Fork the repository and create a feature branch (`git checkout -b feat/pumpfun-v2-decoder`).
   - Test your changes locally using `python cli.py demo`.
   - Ensure linting passes cleanly.
   - Submit a pull request with a concise summary of the rationale and architectural impact.
