# -*- coding: utf-8 -*-
import sqlite3
import sys
import os

# Configurar encoding para Windows
if sys.platform.startswith("win"):
    os.system("chcp 65001 > nul")

db = sqlite3.connect("boletins.db")
db.row_factory = sqlite3.Row

print("DADOS: ANÁLISE TEMPORAL DOS BOLETINS")
print("=" * 40)

# Boletins manuais (que não começam com números como os importados)
cursor = db.execute(
    """
    SELECT numero_boletim, data_coleta, data_validacao,
           CASE
               WHEN numero_boletim LIKE '%.22%' OR numero_boletim LIKE '%.23%' THEN 'Importado'
               ELSE 'Manual'
           END as origem
    FROM boletins
    ORDER BY id
"""
)

boletins = cursor.fetchall()
importados = [b for b in boletins if b["origem"] == "Importado"]
manuais = [b for b in boletins if b["origem"] == "Manual"]

print(f"INFO: BOLETINS IMPORTADOS ({len(importados)}):")
for i, b in enumerate(importados):
    if i < 5:
        print(f'   • {b["numero_boletim"]} - Coleta: {b["data_coleta"]}')
if len(importados) > 5:
    print(f"   ... e mais {len(importados) - 5}")

print(f"\nINFO: BOLETINS MANUAIS ({len(manuais)}):")
for i, b in enumerate(manuais):
    if i < 5:
        print(
            f'   • {b["numero_boletim"]} - Coleta: {b["data_coleta"]} - '
            f'Validação: {b["data_validacao"]}'
        )
if len(manuais) > 5:
    print(f"   ... e mais {len(manuais) - 5}")

print("\nDADOS: CÁLCULO FINAL:")
print(
    f"   • {len(importados)} boletins importados × 15 componentes = {len(importados) * 15}"
)
print(f"   • {len(manuais)} boletins manuais × 15 componentes = {len(manuais) * 15}")
print(f"   • TOTAL: {(len(importados) + len(manuais)) * 15} registros históricos")
print(
    f"   • Confirmado: {len(boletins)} boletins × 15 = {len(boletins) * 15} registros"
)

db.close()
