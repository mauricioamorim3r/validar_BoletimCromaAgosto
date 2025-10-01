#!/usr/bin/env python3
"""
Script para corrigir problemas de acessibilidade no checklist do formulário de cadastro
Adiciona aria-label adequados para todos os selects e inputs do checklist
"""

# Lê o arquivo template
with open('templates/cadastrar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Definir as descrições dos itens do checklist
descriptions = {
    2: "Identificação da amostra",
    3: "Descrição da data de amostragem",
    4: "Descrição da data de recebimento da amostra pelo laboratório",
    5: "Descrição da data de realização das análises",
    6: "Descrição da data de emissão do BRA",
    7: "Identificação do campo produtor ou da instalação",
    8: "Identificação do agente regulado",
    9: "Identificação do ponto de medição e/ou do poço quando aplicável",
    10: "Resultados das análises e normas ou procedimentos utilizados",
    11: "Descrição das características do processo do ponto de amostragem do fluido (pressão e temperatura)",
    12: "Identificação do responsável pela amostragem",
    13: "Indicação dos incertezas de medição, com descrição do nível de confiança e fator de abrangência",
    14: "Identificação dos responsáveis técnicos pela realização da análise",
    15: "Identificação dos responsáveis pela elaboração e aprovação do boletim"
}

# Corrigir os selects de situação (itens 2-15)
for item_num in range(2, 16):
    desc = descriptions[item_num]

    # Padrão para situação
    old_select_situacao = f'<select name="checklist_{item_num}_situacao" class="form-select form-select-sm">'
    new_select_situacao = f'<select name="checklist_{item_num}_situacao" class="form-select form-select-sm" aria-label="Situação do item {item_num} - {desc}">'
    content = content.replace(old_select_situacao, new_select_situacao)

    # Padrão para não aplicável
    old_select_nao_aplicavel = f'<select name="checklist_{item_num}_nao_aplicavel" class="form-select form-select-sm">'
    new_select_nao_aplicavel = f'<select name="checklist_{item_num}_nao_aplicavel" class="form-select form-select-sm" aria-label="Item {item_num} não aplicável - {desc}">'
    content = content.replace(old_select_nao_aplicavel, new_select_nao_aplicavel)

    # Padrão para observação
    old_input_observacao = f'<input type="text" name="checklist_{item_num}_observacao" value="" class="form-control form-control-sm text-center">'
    new_input_observacao = f'<input type="text" name="checklist_{item_num}_observacao" value="" class="form-control form-control-sm text-center" aria-label="Observação do item {item_num} - {desc}">'
    content = content.replace(old_input_observacao, new_input_observacao)

# Salva o arquivo corrigido
with open('templates/cadastrar.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo corrigido com sucesso!")
print("📝 Adicionados aria-labels para todos os campos do checklist (itens 2-15)")
print("🔍 Os itens corrigidos incluem:")
for item_num in range(2, 16):
    print(f"   • Item {item_num}: {descriptions[item_num]}")
