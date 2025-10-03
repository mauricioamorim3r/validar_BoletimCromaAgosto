#!/usr/bin/env python3
"""
Hotfix temporário para o erro de relatório
Desabilita cálculos CEP temporariamente para identificar a causa
"""

def create_hotfix_route(app, get_db):
    """Cria uma rota de hotfix sem cálculos CEP"""
    
    @app.route('/relatorio/<int:boletim_id>/hotfix')
    def relatorio_hotfix(boletim_id):
        """Relatório sem cálculos CEP para identificar problema"""
        from flask import render_template
        
        try:
            db = get_db()
            
            # Buscar dados básicos
            boletim = db.execute(
                'SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
            
            if boletim is None:
                from flask import flash, redirect, url_for
                flash('Boletim não encontrado!')
                return redirect(url_for('listar_boletins'))
            
            # Buscar componentes SEM cálculos CEP
            componentes = db.execute('''
                SELECT * FROM componentes WHERE boletin_id = ?
            ''', (boletim_id,)).fetchall()
            
            # Converter para dicionário simples
            componentes_simples = []
            for comp in componentes:
                comp_dict = dict(comp)
                comp_dict['cep_lci'] = None  # Desabilitar CEP
                comp_dict['cep_lcs'] = None  # Desabilitar CEP
                componentes_simples.append(comp_dict)
            
            # Buscar outros dados
            propriedades = db.execute('''
                SELECT * FROM propriedades WHERE boletin_id = ?
            ''', (boletim_id,)).fetchall()
            
            checklist = db.execute('''
                SELECT * FROM checklist_itens WHERE boletin_id = ? ORDER BY item_numero
            ''', (boletim_id,)).fetchall()
            
            # Criar componentes_dict sem CEP
            mapeamento_nomes = {
                'Metano, CH₄': 'metano_ch4',
                'Etano, C₂H₆': 'etano_c2h6',
                'Propano, C₃H₈': 'propano_c3h8',
                'i-Butano, i-C₄H₁₀': 'i_butano_ic4h10',
                'n-Butano, n-C₄H₁₀': 'n_butano_nc4h10',
                'i-Pentano, i-C₅H₁₂': 'i_pentano_ic5h12',
                'n-Pentano, n-C₅H₁₂': 'n_pentano_nc5h12',
                'C₆+': 'c6_mais',
                'Heptano': 'heptano',
                'Octano': 'octano',
                'Nonano': 'nonano',
                'Decano': 'decano',
                'Oxigênio, O₂': 'oxigenio_o2',
                'Nitrogênio, N₂': 'nitrogenio_n2',
                'Dióxido de Carbono, CO₂': 'dioxido_carbono_co2'
            }
            
            componentes_dict = {}
            for comp in componentes:
                nome_template = mapeamento_nomes.get(comp['nome'])
                if nome_template:
                    componentes_dict[nome_template] = comp['percentual_molar']
            
            # Validação ANP simplificada
            validacao_prazos = {
                'coleta_emissao': {'status': 'OK', 'dias_decorridos': 0},
                'emissao_validacao': {'status': 'OK', 'dias_decorridos': 0},
                'prazo_total': {'status': 'OK', 'dias_decorridos': 0}
            }
            
            db.close()
            
            return render_template(
                'relatorio_excel.html',
                boletim=boletim,
                componentes=componentes_simples,
                propriedades=propriedades,
                checklist=checklist,
                componentes_dict=componentes_dict,
                edit_mode=False,
                validacao_prazos=validacao_prazos
            )
            
        except Exception as e:
            import logging
            logging.error(f"Erro no hotfix do relatório {boletim_id}: {e}")
            return f"""
            <h1>❌ Erro no Hotfix</h1>
            <p><strong>Erro:</strong> {str(e)}</p>
            <p>Isso indica um problema mais fundamental.</p>
            <p><a href="/dashboard">Voltar ao Dashboard</a></p>
            """