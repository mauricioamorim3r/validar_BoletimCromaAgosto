import json

with open('accessibility-audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('🎯 Score de Acessibilidade:', data['categories']['accessibility'].get('score', 'N/A'))
print('\n📊 Auditorias com problemas:')
problemas = 0
for audit_id, audit in data['audits'].items():
    if audit.get('score') == 0 and 'details' in audit and audit['details'].get('items'):
        print(f'  ❌ {audit["title"]}: {len(audit["details"]["items"])} problema(s)')
        problemas += len(audit['details']['items'])

print(f'\n📈 Total de problemas encontrados: {problemas}')

# Verificar especificamente os problemas de label
print('\n🏷️  Problemas de Labels:')
button_issues = data['audits'].get('button-name', {})
if button_issues.get('score') == 0:
    print(f'  - Buttons sem nome acessível: {len(button_issues.get("details", {}).get("items", []))} problema(s)')
    for item in button_issues.get('details', {}).get('items', []):
        print(f'    → {item["node"]["snippet"]}')
