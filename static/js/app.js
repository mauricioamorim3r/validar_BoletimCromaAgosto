document.addEventListener('DOMContentLoaded', function() {
    // Lista de componentes para validação
    const componentes = [
        'Metano', 'Etano', 'Propano', 'i-Butano', 'n-Butano', 
        'i-Pentano', 'n-Pentano', 'Hexano', 'Heptano', 'Octano', 
        'Nonano', 'Decano', 'Oxigênio', 'Nitrogênio', 'CO2'
    ];
    
    // Adicionar listeners para todos os componentes
    componentes.forEach(componente => {
        const input = document.getElementById(componente);
        if (input) {
            input.addEventListener('input', function() {
                validateComponent(this.id);
                updateTotalPercentage();
            });
        }
    });
    
    function validateComponent(componentId) {
        const input = document.getElementById(componentId);
        const value = parseFloat(input.value) || 0;
        const statusSpan = document.getElementById('status_' + componentId);
        
        // Limites A.G.A #8
        const limits = {
            'Metano': { min: 0, max: 100 },
            'Etano': { min: 0, max: 100 },
            'Propano': { min: 0, max: 12 },
            'i-Butano': { min: 0, max: 6 },
            'n-Butano': { min: 0, max: 6 },
            'i-Pentano': { min: 0, max: 4 },
            'n-Pentano': { min: 0, max: 4 },
            'Hexano': { min: 0, max: 100 },
            'Heptano': { min: 0, max: 100 },
            'Octano': { min: 0, max: 100 },
            'Nonano': { min: 0, max: 100 },
            'Decano': { min: 0, max: 100 },
            'Oxigênio': { min: 0, max: 21 },
            'Nitrogênio': { min: 0, max: 100 },
            'CO2': { min: 0, max: 100 }
        };
        
        const limit = limits[componentId];
        
        if (limit && statusSpan) {
            if (value >= limit.min && value <= limit.max) {
                statusSpan.textContent = 'VALIDADO';
                statusSpan.className = 'status-validado';
                input.style.borderColor = '#28a745';
            } else {
                statusSpan.textContent = 'INVALIDADO';
                statusSpan.className = 'status-invalidado';
                input.style.borderColor = '#dc3545';
            }
        }
    }
    
    // Função para calcular e mostrar total de percentuais
    function updateTotalPercentage() {
        let total = 0;
        componentes.forEach(componente => {
            const input = document.getElementById(componente);
            if (input && input.value) {
                total += parseFloat(input.value) || 0;
            }
        });
        
        // Mostrar total (criar elemento se não existir)
        let totalDisplay = document.getElementById('totalPercentage');
        if (!totalDisplay) {
            totalDisplay = document.createElement('div');
            totalDisplay.id = 'totalPercentage';
            totalDisplay.style.cssText = 'position: fixed; top: 10px; right: 10px; background: #007bff; color: white; padding: 10px; border-radius: 5px; font-weight: bold; z-index: 1000;';
            document.body.appendChild(totalDisplay);
        }
        
        totalDisplay.innerHTML = `Total: ${total.toFixed(3)}%`;
        totalDisplay.style.backgroundColor = (total >= 99.5 && total <= 100.5) ? '#28a745' : '#dc3545';
    }
    
    // Validação da soma dos percentuais no submit
    const cadastroForm = document.getElementById('cadastroForm');
    if (cadastroForm) {
        cadastroForm.addEventListener('submit', function(e) {
            let totalPercent = 0;
            
            componentes.forEach(componente => {
                const input = document.getElementById(componente);
                if (input && input.value) {
                    totalPercent += parseFloat(input.value) || 0;
                }
            });
            
            if (Math.abs(totalPercent - 100) > 2) {
                e.preventDefault();
                alert(`A soma dos percentuais dos componentes deve ser aproximadamente 100%. 
                       Atualmente: ${totalPercent.toFixed(3)}%
                       
                       Por favor, ajuste os valores antes de continuar.`);
                return false;
            }
            
            // Validar campos obrigatórios
            const requiredFields = cadastroForm.querySelectorAll('[required]');
            let hasEmptyFields = false;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc3545';
                    hasEmptyFields = true;
                } else {
                    field.style.borderColor = '#28a745';
                }
            });
            
            if (hasEmptyFields) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios.');
                return false;
            }
        });
    }
    
    // Validação de campos obrigatórios
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.value) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
});