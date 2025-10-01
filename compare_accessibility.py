import json

with open('accessibility-audit-fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('🎯 Score de Acessibilidade CORRIGIDO:', data['categories']['accessibility'].get('score', 'N/A'))
print('\n📊 Auditorias com problemas:')
problemas = 0
for audit_id, audit in data['audits'].items():
    if audit.get('score') == 0 and 'details' in audit and audit['details'].get('items'):
        print(f'  ❌ {audit["title"]}: {len(audit["details"]["items"])} problema(s)')
        problemas += len(audit['details']['items'])

print(f'\n📈 Total de problemas restantes: {problemas}')

# Comparação
print('\n📊 COMPARAÇÃO:')
print('Score ANTES das correções: 0.91 (91/100)')
print(f'Score APÓS as correções: {data["categories"]["accessibility"].get("score", "N/A")}')
