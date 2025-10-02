# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application for validating chromatographic analysis bulletins in the oil and gas industry. The system implements AGA #8 methodology and Statistical Process Control (CEP) for validating gas component analysis results, with ANP compliance tracking per Portaria 52.

## Commands

### Development
```bash
# Install all dependencies
pip install -r requirements.txt

# Run the application (default port 3000)
python app.py

# Access the application
# Open browser to http://127.0.0.1:3000
```

### Build & Distribution
```bash
# Complete build with validation
python build.py

# Run tests and verification
python test_funcionalidades.py
python verificar_cep.py

# Check database integrity
python check_db.py
```

### Database Management
- SQLite database at `boletins.db` (auto-created)
- Initialize: `init_db()` function in `app.py`
- Debug: `python debug_boletim.py` or `python check_fields.py`

## Architecture Overview

### MVC Structure
- **Model**: SQLite database with 4 tables (`boletins`, `componentes`, `propriedades`, `historico_componentes`)
- **View**: Jinja2 templates with Excel-inspired UI and glassmorphism design
- **Controller**: Flask routes in `app.py` with modular validation logic

### Core Modules
- **`app.py`**: Main Flask application with routes and database functions
- **`config.py`**: Configuration constants (AGA#8 limits, CEP parameters, company info)
- **`excel_import.py`**: Excel file processing for bulk bulletin imports
- **`validacao_prazos_anp.py`**: ANP Portaria 52 compliance validation (25-day limit)
- **`build.py`**: Production build system with distribution packaging

### Database Schema
- `boletins`: Main bulletin data with metadata and process conditions
- `componentes`: Gas components (15 types) with percentual values and validation status
- `propriedades`: Fluid properties (compressibility factor, specific mass, molecular mass)
- `historico_componentes`: Historical component values for CEP calculations

### Triple Validation System
1. **AGA #8 Validation**: Component percentages against industry limits (configurable in `config.py`)
2. **CEP Validation**: Statistical process control using last 8 samples (d2 = 1.128)
3. **ANP Compliance**: 25-day collection-to-emission timeline per Portaria 52

### Template Structure
Key templates in `/templates/`:
- `base.html`: Base template with glassmorphism navigation
- `dashboard.html`: Analytics dashboard with statistics and charts
- `main.html`: Main bulletin listing with tabbed interface
- `cadastrar.html`: Bulletin registration form with real-time validation
- `editar_boletim.html`: Edit bulletin interface
- `relatorio.html` & `relatorio_excel.html`: Validation reports with PDF export
- `importar_excel.html`: Bulk import interface

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
1. **Registration**: User registers bulletin via form or Excel import
2. **AGA #8 Validation**: System validates each component against industry limits
3. **CEP Validation**: Statistical process control using historical data (≥8 previous samples)
4. **ANP Compliance**: Timeline validation per Portaria 52 (25-day collection-to-emission)
5. **Status Determination**: Overall bulletin status (VALIDATED/INVALIDATED/PENDING)
6. **Historical Storage**: Data stored for future CEP calculations and trend analysis
7. **Report Generation**: PDF reports with validation details and recommendations

## Key Technical Details

### Configuration Management
- All limits and constants defined in `config.py`
- AGA #8 limits: Configurable per component (e.g., Propane: 0-12%, O₂: 0-21%)
- CEP parameters: 8-sample minimum, d2=1.128 constant, 3-sigma limits
- Company branding: BRAVA ENERGIA, Campo de Atalaia

### Frontend Architecture
- Glassmorphism design system following user's design standards
- Real-time validation with JavaScript (±2% sum tolerance)
- Excel-inspired table styling with conditional formatting
- Bootstrap 5 + custom CSS with gradients and backdrop-filter effects

### Excel Import System
- Structured template: 'Boletins', 'Componentes', 'Propriedades' sheets
- Batch processing with error handling and validation reports
- Function: `processar_excel_boletins()` in `excel_import.py`

### PDF Report Generation
- ReportLab integration for professional reports
- Company branding and regulatory compliance formatting
- Embedded validation charts and statistical analysis

## Development & Testing

### Dependencies (requirements.txt)
- Flask==2.3.3
- reportlab==4.0.4 (PDF generation)
- pandas==2.0.3 (Excel processing)
- openpyxl==3.1.2 (Excel file handling)
- Werkzeug==2.3.7

### Debug & Validation Scripts
- `test_funcionalidades.py`: Server connectivity and route testing
- `verificar_cep.py`: CEP algorithm validation
- `check_db.py`, `debug_boletim.py`: Database integrity checks
- `analise_temporal.py`: Historical data analysis
- `analisar_discrepancia.py`: Data quality analysis

### Technical Constraints
- Component percentages sum: 100% (±2% tolerance per `config.TOLERANCIA_SOMA_PERCENTUAL`)
- CEP validation: Minimum 8 historical samples (`config.CEP_AMOSTRAS_MIN`)
- ANP compliance: 25-day collection-to-emission maximum
- All 15 gas components required per bulletin
- Foreign key constraints with CASCADE delete maintain data integrity
