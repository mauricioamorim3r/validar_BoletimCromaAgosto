# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application for validating chromatographic analysis bulletins in the oil and gas industry. The system implements AGA #8 methodology and Statistical Process Control (CEP) for validating gas component analysis results.

## Commands

### Development
```bash
# Install dependencies
pip install flask

# Run the application
python app.py

# Access the application
# Open browser to http://localhost:5000
```

### Database
- The application uses SQLite with automatic database initialization
- Database file: `boletins.db` (created automatically on first run)
- No manual database setup required - tables are created via `init_db()` function

## Architecture Overview

### MVC Structure
- **Model**: SQLite database with 4 tables (`boletins`, `componentes`, `propriedades`, `historico_componentes`)
- **View**: Jinja2 templates in `/templates` directory with Excel-inspired UI
- **Controller**: Flask routes in `app.py` with validation logic

### Key Components

#### Database Schema
- `boletins`: Main bulletin data with metadata and process conditions
- `componentes`: Gas components (15 types) with percentual values and validation status
- `propriedades`: Fluid properties (compressibility factor, specific mass, molecular mass)
- `historico_componentes`: Historical component values for CEP calculations

#### Validation System
1. **AGA #8 Validation** (`valida_aga8()`): Validates component percentages against industry limits
2. **CEP Validation** (`valida_cep()`): Statistical process control using last 8 samples, mobile range, and control limits (d2 = 1.128)

### File Structure
- `app.py`: Main Flask application with routes, database functions, and validation logic
- `templates/`: Jinja2 HTML templates
  - `base.html`: Base template with navigation
  - `main.html`: Dashboard with tabs (bulletins list, history)
  - `cadastrar.html`: Bulletin registration form
  - `relatorio.html`: Validation report display
- `static/css/style.css`: Excel-inspired styling
- `static/js/app.js`: Real-time validation and form interactions

### Component Validation Rules
The system validates 15 gas components against AGA #8 limits:
- Methane, Ethane: 0-100%
- Propane: 0-12%
- i-Butane, n-Butane: 0-6%
- i-Pentane, n-Pentane: 0-4%
- Hexane through Decano: 0-100%
- Oxygen: 0-21%
- Nitrogen, CO2: 0-100%

### Business Logic Flow
1. User registers bulletin with component percentages
2. System validates each component against AGA #8 limits
3. System performs CEP validation using historical data (requires ≥2 previous samples)
4. System determines overall bulletin status (VALIDATED/INVALIDATED)
5. System stores historical data for future CEP calculations
6. System generates validation report

## Development Notes

### Frontend Styling
- Uses Bootstrap 5 with custom Excel-inspired CSS
- Segoe UI font family for Windows-native appearance
- Color scheme: Primary blue (#0d6efd), success green, danger red
- Responsive design with mobile breakpoints

### Real-time Validation
- JavaScript validates component limits as user types
- Form submission blocked if component sum ≠ 100% (±2% tolerance)
- Required field validation with visual feedback

### Database Relationships
- Foreign key constraints with CASCADE delete
- `boletin_id` links components and properties to bulletins
- Historical data preserved for CEP calculations across bulletins

## Technical Constraints

### Validation Requirements
- Component percentages must sum to ~100% (±2% tolerance)
- CEP requires minimum 2 historical samples for validation
- All 15 gas components must be provided for each bulletin
- AGA #8 validation is mandatory for all components

### Data Integrity
- SQLite row factory ensures consistent data access
- Automatic timestamp generation for validation dates
- Foreign key constraints maintain referential integrity