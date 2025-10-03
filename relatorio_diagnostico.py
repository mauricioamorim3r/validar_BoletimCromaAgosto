#!/usr/bin/env python3
"""
Rota de relatório simplificada para diagnóstico de problemas
Sistema de Validação de Boletins - SGM
"""

from flask import render_template_string

def create_simple_report_route(app, get_db):
    """Cria uma rota de relatório simplificada para diagnóstico"""
    
    @app.route('/relatorio/<int:boletim_id>/simple')
    def relatorio_simple(boletim_id):
        """Versão simplificada do relatório para diagnóstico"""
        
        try:
            db = get_db()
            
            # Buscar apenas dados básicos do boletim
            boletim = db.execute(
                'SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
            
            if boletim is None:
                return f"<h1>Boletim {boletim_id} não encontrado</h1>"
            
            # Buscar componentes sem cálculos CEP
            componentes = db.execute('''
                SELECT * FROM componentes WHERE boletin_id = ?
            ''', (boletim_id,)).fetchall()
            
            # Template HTML simplificado
            template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Relatório Simplificado - Boletim {{ boletim.numero_boletim }}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                    .error { color: red; font-weight: bold; }
                    .success { color: green; font-weight: bold; }
                </style>
            </head>
            <body>
                <h1>🧪 Relatório Simplificado - Diagnóstico</h1>
                <div class="success">✅ Conexão com banco de dados: OK</div>
                <div class="success">✅ Boletim encontrado: {{ boletim.numero_boletim }}</div>
                <div class="success">✅ Componentes carregados: {{ componentes|length }}</div>
                
                <h2>📋 Dados do Boletim</h2>
                <table>
                    <tr><th>Campo</th><th>Valor</th></tr>
                    <tr><td>ID</td><td>{{ boletim.id }}</td></tr>
                    <tr><td>Número</td><td>{{ boletim.numero_boletim }}</td></tr>
                    <tr><td>Data Coleta</td><td>{{ boletim.data_coleta }}</td></tr>
                    <tr><td>Data Emissão</td><td>{{ boletim.data_emissao }}</td></tr>
                    <tr><td>Classificação</td><td>{{ boletim.classificacao }}</td></tr>
                    <tr><td>Pressão</td><td>{{ boletim.pressao }} atm</td></tr>
                    <tr><td>Temperatura</td><td>{{ boletim.temperatura }} °C</td></tr>
                </table>
                
                <h2>🧪 Componentes</h2>
                <table>
                    <tr><th>Nome</th><th>% Molar</th><th>Status AGA</th><th>Status CEP</th></tr>
                    {% for comp in componentes %}
                    <tr>
                        <td>{{ comp.nome }}</td>
                        <td>{{ comp.percentual_molar }}</td>
                        <td>{{ comp.status_aga }}</td>
                        <td>{{ comp.status_cep }}</td>
                    </tr>
                    {% endfor %}
                </table>
                
                <h2>🔧 Status do Sistema</h2>
                <div class="success">✅ Relatório simplificado funcionando</div>
                <div>⚠️ Esta é uma versão de diagnóstico sem cálculos CEP</div>
                <div>🔗 <a href="/relatorio/{{ boletim.id }}">Tentar relatório completo</a></div>
                <div>🏠 <a href="/dashboard">Voltar ao Dashboard</a></div>
            </body>
            </html>
            """
            
            db.close()
            
            return render_template_string(template, 
                                        boletim=boletim, 
                                        componentes=componentes)
                                        
        except Exception as e:
            return f"""
            <h1>❌ Erro no Relatório Simplificado</h1>
            <p><strong>Erro:</strong> {str(e)}</p>
            <p>Este erro indica um problema mais fundamental no sistema.</p>
            <p><a href="/dashboard">Voltar ao Dashboard</a></p>
            """