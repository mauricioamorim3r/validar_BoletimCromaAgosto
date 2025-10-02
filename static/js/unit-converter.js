// Conversões de Unidades - Sistema de Validação de Boletins
// Suporte para conversões de temperatura e pressão

/**
 * Conversões de Temperatura
 */
const TemperatureConverter = {
    // Conversões para Celsius (unidade base)
    toCelsius: {
        celsius: (value) => value,
        kelvin: (value) => value - 273.15,
        fahrenheit: (value) => (value - 32) * 5/9
    },
    
    // Conversões de Celsius para outras unidades
    fromCelsius: {
        celsius: (value) => value,
        kelvin: (value) => value + 273.15,
        fahrenheit: (value) => (value * 9/5) + 32
    },
    
    convert: function(value, fromUnit, toUnit) {
        if (fromUnit === toUnit) return value;
        
        // Primeiro converte para Celsius (unidade base)
        const celsius = this.toCelsius[fromUnit](value);
        
        // Depois converte de Celsius para unidade desejada
        return this.fromCelsius[toUnit](celsius);
    }
};

/**
 * Conversões de Pressão
 */
const PressureConverter = {
    // Conversões para Pa (Pascal - unidade base)
    toPascal: {
        pa: (value) => value,
        kpa: (value) => value * 1000,
        bar: (value) => value * 100000,
        atm: (value) => value * 101325,
        psi: (value) => value * 6894.76
    },
    
    // Conversões de Pascal para outras unidades
    fromPascal: {
        pa: (value) => value,
        kpa: (value) => value / 1000,
        bar: (value) => value / 100000,
        atm: (value) => value / 101325,
        psi: (value) => value / 6894.76
    },
    
    convert: function(value, fromUnit, toUnit) {
        if (fromUnit === toUnit) return value;
        
        // Primeiro converte para Pascal (unidade base)
        const pascal = this.toPascal[fromUnit](value);
        
        // Depois converte de Pascal para unidade desejada
        return this.fromPascal[toUnit](pascal);
    }
};

/**
 * Configuração das unidades disponíveis
 */
const UnitsConfig = {
    temperature: {
        celsius: { name: '°C', symbol: '°C', default: true },
        kelvin: { name: 'K', symbol: 'K', default: false }
    },
    
    pressure: {
        atm: { name: 'atm', symbol: 'atm', default: true },
        kpa: { name: 'kPa', symbol: 'kPa', default: false },
        pa: { name: 'Pa', symbol: 'Pa', default: false },
        bar: { name: 'bar', symbol: 'bar', default: false },
        psi: { name: 'psi', symbol: 'psi', default: false }
    }
};

/**
 * Inicialização dos seletores de unidade
 */
function initializeUnitSelectors() {
    // Inicializar seletor de temperatura
    const temperatureGroup = document.querySelector('[data-unit-group="temperature"]');
    if (temperatureGroup) {
        setupUnitSelector(temperatureGroup, 'temperature', TemperatureConverter);
    }
    
    // Inicializar seletor de pressão
    const pressureGroup = document.querySelector('[data-unit-group="pressure"]');
    if (pressureGroup) {
        setupUnitSelector(pressureGroup, 'pressure', PressureConverter);
    }
}

/**
 * Configura um seletor de unidade
 */
function setupUnitSelector(container, unitType, converter) {
    const input = container.querySelector('input[type="number"]');
    const selector = container.querySelector('.unit-selector');
    const display = container.querySelector('.unit-display');
    
    if (!input || !selector) return;
    
    const units = UnitsConfig[unitType];
    let currentUnit = Object.keys(units).find(key => units[key].default);
    let currentValue = 0;
    
    // Criar opções do seletor
    Object.entries(units).forEach(([key, config]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = config.symbol;
        option.selected = config.default;
        selector.appendChild(option);
    });
    
    // Atualizar display da unidade
    function updateUnitDisplay() {
        if (display) {
            display.textContent = units[currentUnit].symbol;
        }
    }
    
    // Handler para mudança de unidade
    selector.addEventListener('change', function() {
        const newUnit = this.value;
        const inputValue = parseFloat(input.value);
        
        if (!isNaN(inputValue) && inputValue !== 0) {
            // Converter valor da unidade atual para nova unidade
            const convertedValue = converter.convert(inputValue, currentUnit, newUnit);
            input.value = convertedValue.toFixed(2);
        }
        
        currentUnit = newUnit;
        updateUnitDisplay();
        
        // Atualizar campo hidden se existir
        const hiddenUnit = container.querySelector(`input[name="${input.name}_unit"]`);
        if (hiddenUnit) {
            hiddenUnit.value = currentUnit;
        }
    });
    
    // Handler para mudança de valor
    input.addEventListener('input', function() {
        currentValue = parseFloat(this.value) || 0;
    });
    
    // Inicializar display
    updateUnitDisplay();
}

/**
 * Validação de valores de unidade
 */
function validateUnitValue(value, unitType, unit) {
    const numValue = parseFloat(value);
    
    if (isNaN(numValue)) {
        return { valid: false, message: 'Valor deve ser numérico' };
    }
    
    // Validações específicas por tipo de unidade
    if (unitType === 'temperature') {
        // Temperatura não pode ser menor que zero absoluto
        const celsiusValue = TemperatureConverter.convert(numValue, unit, 'celsius');
        if (celsiusValue < -273.15) {
            return { valid: false, message: 'Temperatura não pode ser menor que zero absoluto (-273.15°C)' };
        }
    }
    
    if (unitType === 'pressure') {
        // Pressão não pode ser negativa
        if (numValue < 0) {
            return { valid: false, message: 'Pressão não pode ser negativa' };
        }
    }
    
    return { valid: true, message: '' };
}

/**
 * Obter valor convertido para unidade padrão
 */
function getStandardValue(container, unitType, converter) {
    const input = container.querySelector('input[type="number"]');
    const selector = container.querySelector('.unit-selector');
    
    if (!input || !selector) return null;
    
    const value = parseFloat(input.value);
    const currentUnit = selector.value;
    
    if (isNaN(value)) return null;
    
    // Definir unidades padrão
    const standardUnits = {
        temperature: 'celsius',
        pressure: 'atm'
    };
    
    const standardUnit = standardUnits[unitType];
    return converter.convert(value, currentUnit, standardUnit);
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    initializeUnitSelectors();
});

// Exportar para uso global
window.TemperatureConverter = TemperatureConverter;
window.PressureConverter = PressureConverter;
window.UnitsConfig = UnitsConfig;
window.validateUnitValue = validateUnitValue;
window.getStandardValue = getStandardValue;