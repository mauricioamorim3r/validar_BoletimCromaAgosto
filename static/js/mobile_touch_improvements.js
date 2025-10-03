// Melhorias Mobile - Touch Interactions
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Iniciando melhorias mobile touch-friendly...');
    
    // 1. Touch feedback para todos os botões
    const buttons = document.querySelectorAll('.btn, .action-btn, button');
    buttons.forEach(btn => {
        btn.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
            this.style.transition = 'transform 0.1s ease';
        });
        
        btn.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });
    
    // 2. Melhorar swipe em tabelas
    const tableContainers = document.querySelectorAll('.table-responsive');
    tableContainers.forEach(container => {
        let startX = 0;
        let scrollLeft = 0;
        let isScrolling = false;
        
        container.addEventListener('touchstart', function(e) {
            startX = e.touches[0].pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
            isScrolling = true;
            container.style.cursor = 'grabbing';
        });
        
        container.addEventListener('touchmove', function(e) {
            if (!isScrolling) return;
            e.preventDefault();
            const x = e.touches[0].pageX - container.offsetLeft;
            const walk = (x - startX) * 2;
            container.scrollLeft = scrollLeft - walk;
        });
        
        container.addEventListener('touchend', function() {
            isScrolling = false;
            container.style.cursor = 'grab';
            
            // Mostrar indicador de mais conteúdo se necessário
            if (container.scrollLeft < container.scrollWidth - container.clientWidth - 10) {
                showScrollHint(container);
            }
        });
    });
    
    // 3. Indicador visual de scroll
    function showScrollHint(container) {
        const hint = container.querySelector('.scroll-hint');
        if (hint) {
            hint.style.opacity = '1';
            setTimeout(() => {
                hint.style.opacity = '0';
            }, 2000);
        }
    }
    
    // 4. Auto-resize textarea com melhor UX mobile
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.max(this.scrollHeight, 44) + 'px';
        });
        
        // Touch feedback
        textarea.addEventListener('focus', function() {
            this.style.borderColor = '#3b82f6';
            this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
        });
        
        textarea.addEventListener('blur', function() {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        });
    });
    
    // 5. Melhorar select em mobile
    const selects = document.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('focus', function() {
            // Scroll para o elemento em foco
            setTimeout(() => {
                this.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
            }, 300);
        });
    });
    
    // 6. Toast notifications mobile-friendly
    function showMobileToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `mobile-toast mobile-toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 9999;
            max-width: 90vw;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideUpFadeIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideDownFadeOut 0.3s ease forwards';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }
    
    // 7. Detectar orientação e ajustar
    function handleOrientationChange() {
        setTimeout(() => {
            // Reajustar tabelas após mudança de orientação
            tableContainers.forEach(container => {
                container.scrollLeft = 0;
            });
            
            // Reajustar modal se aberto
            const modal = document.querySelector('.modal.show');
            if (modal) {
                modal.style.paddingTop = window.innerHeight < 600 ? '10px' : '50px';
            }
        }, 100);
    }
    
    window.addEventListener('orientationchange', handleOrientationChange);
    window.addEventListener('resize', handleOrientationChange);
    
    // 8. Melhorar navegação por formulário em mobile
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach((input, index) => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && this.type !== 'textarea') {
                e.preventDefault();
                const nextInput = formInputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                    nextInput.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                }
            }
        });
    });
    
    // 9. Adicionar estilos de animação CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUpFadeIn {
            from { 
                opacity: 0; 
                transform: translateX(-50%) translateY(20px); 
            }
            to { 
                opacity: 1; 
                transform: translateX(-50%) translateY(0); 
            }
        }
        
        @keyframes slideDownFadeOut {
            from { 
                opacity: 1; 
                transform: translateX(-50%) translateY(0); 
            }
            to { 
                opacity: 0; 
                transform: translateX(-50%) translateY(20px); 
            }
        }
        
        .table-responsive {
            cursor: grab;
        }
        
        .table-responsive:active {
            cursor: grabbing;
        }
        
        @media (max-width: 768px) {
            .modal-dialog {
                margin: 10px;
                max-width: calc(100vw - 20px);
            }
            
            .modal-content {
                border-radius: 12px;
            }
            
            .modal-header {
                padding: 1rem;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .modal-body {
                padding: 1rem;
                max-height: 70vh;
                overflow-y: auto;
            }
            
            .modal-footer {
                padding: 1rem;
                border-top: 1px solid #e5e7eb;
            }
        }
    `;
    document.head.appendChild(style);
    
    console.log('✅ Melhorias mobile aplicadas com sucesso!');
    
    // Expor função toast globalmente
    window.showMobileToast = showMobileToast;
});