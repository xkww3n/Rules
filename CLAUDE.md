# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a rule management system for network proxy software, generating rulesets in multiple formats for various proxy applications. The system fetches and processes rules from upstream sources (including v2fly community and AdGuard filters) and generates optimized rulesets for different proxy software.

## Development Commands

### Build System
- `pdm run build` - Build all rulesets (main entry point via main.py)
- `pdm run debug` - Run build in debug mode with DEBUG=1 environment variable
- `pdm run profile` - Profile the build process

### Testing
- `pdm run test` - Run all tests
- `pytest tests/test_0_rule.py` - Run specific test file
- `pytest tests/test_0_rule.py::Test::test_type_checking_init` - Run specific test
- `pytest --cov` - Run tests with coverage report

### Dependency Management
- `pdm install` - Install all dependencies
- `pdm add <package>` - Add new dependency
- `pdm update` - Update dependencies

## Architecture

### Core Components

1. **Workers System** (workers/)
   - Each worker module in `workers/` directory contains a `build()` function
   - Workers are dynamically loaded and executed by `main.py`
   - Key workers:
     - `v2fly.py` - Processes v2fly community rulesets
     - `domestic_domain.py` - Handles domestic domain rules
     - `domestic_cidr.py` - Handles domestic IP CIDR rules
     - `reject_exclude.py` - Processes ad blocking and exclusion rules
     - `custom.py` - Handles custom rules from source/ directory

2. **Models** (models/)
   - `Rule` class - Represents individual rules with types (DomainSuffix, DomainFull, IPCIDR, etc.)
   - `RuleSet` class - Container for rules with deduplication and sorting capabilities
   - Rule types support inclusion checking to optimize ruleset size

3. **Utils** (utils/)
   - `geosite.py` - Generates rulesets in various formats from v2fly geosite data
   - `rule.py` - Rule loading, dumping, and manipulation utilities
   - `ruleset.py` - RuleSet operations including format conversion
   - `log_decorator.py` - Logging utilities for worker functions

4. **Output Formats** (dists/)
   - `text/` - Plain text rules (Surge standard, dot wildcard)
   - `text-plus/` - Enhanced text format
   - `quantumult/` - Clash format (plus wildcard)
   - `classical/` - Legacy Surge format
   - `yaml/` - YAML rulesets
   - `geosite/` - V2Ray GeoSite database
   - `sing-ruleset/` - sing-box JSON rulesets

### Data Flow

1. Workers fetch data from upstream sources (config.py URLs) or local source files
2. Data is parsed into Rule and RuleSet objects
3. Rules are deduplicated and optimized (removing redundant rules)
4. Output is generated in multiple formats to dists/ directory

### Key Configuration

- `config.py` contains:
  - `TARGETS` - List of output formats to generate
  - `LIST_REJECT_URL` - AdBlock filter sources
  - `LIST_EXCL_URL` - Whitelist sources
  - Path configurations for source and distribution directories

### Rule Processing

- Rules support inclusion checking (e.g., `*.example.com` includes `sub.example.com`)
- Automatic deduplication removes redundant rules
- Sorting ensures optimal rule matching order (suffixes before full domains)

## Important Notes

- The project uses PDM for dependency management (Python 3.11 required)
- Workers are executed in alphabetical order but should be independent
- Debug mode can be enabled with `DEBUG=1` environment variable for verbose logging
- The system processes both domain rules and IP CIDR rules
- Output formats are optimized for different proxy software compatibility