import React, { useState } from 'react';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { StatisticsTable } from './StatisticsTable';

interface CromatografiaData {
  id: string;
  dataColeta: string;
  dataRelatorio: string;
  validacao: string;
  boletim: string;
  resultado: number;
  etanol: number;
  propanol: number;
  isobutanol: number;
  nbutanol: number;
  isopenthanol: number;
  penthanol: number;
  hexanol: number;
  heptanol: number;
  octanol: number;
  nonanol: number;
  decanol: number;
  undecanol: number;
  dodecanol: number;
  tridecanol: number;
  tetradecanol: number;
  [key: string]: any;
}

export function CromatografiaValidation() {
  const [data, setData] = useState<CromatografiaData[]>([]);
  const [editingCell, setEditingCell] = useState<{ rowIndex: number; field: string } | null>(null);

  // Dados de exemplo baseados na planilha
  const sampleData: CromatografiaData[] = [
    {
      id: '1',
      dataColeta: '29/05/2019',
      dataRelatorio: '27/06/2019',
      validacao: '27/06/2019',
      boletim: '545.19.156.00',
      resultado: 99.63,
      etanol: 0.003,
      propanol: 0.003,
      isobutanol: 0.002,
      nbutanol: 0.003,
      isopenthanol: 0.002,
      penthanol: 0.001,
      hexanol: 0.001,
      heptanol: 0.001,
      octanol: 0.002,
      nonanol: 0.002,
      decanol: 0.002,
      undecanol: 0.002,
      dodecanol: 0.002,
      tridecanol: 0.002,
      tetradecanol: 0.001
    },
    // Adicionar mais dados de exemplo...
  ];

  React.useEffect(() => {
    setData(sampleData);
  }, []);

  const handleCellEdit = (rowIndex: number, field: string, value: string) => {
    const newData = [...data];
    if (newData[rowIndex]) {
      if (field === 'resultado' || field.includes('anol')) {
        newData[rowIndex][field] = parseFloat(value) || 0;
      } else {
        newData[rowIndex][field] = value;
      }
      setData(newData);
    }
  };

  const addNewRow = () => {
    const newRow: CromatografiaData = {
      id: Date.now().toString(),
      dataColeta: '',
      dataRelatorio: '',
      validacao: '',
      boletim: '',
      resultado: 0,
      etanol: 0,
      propanol: 0,
      isobutanol: 0,
      nbutanol: 0,
      isopenthanol: 0,
      penthanol: 0,
      hexanol: 0,
      heptanol: 0,
      octanol: 0,
      nonanol: 0,
      decanol: 0,
      undecanol: 0,
      dodecanol: 0,
      tridecanol: 0,
      tetradecanol: 0
    };
    setData([...data, newRow]);
  };

  return (
    <Card className="rounded-t-none border-t-0">
      <div className="p-4">
        {/* Cabeçalho da Seção */}
        <div className="bg-blue-800 text-white p-3 mb-4 rounded">
          <h2 className="text-center">PLANILHA DE VALIDAÇÃO DE CROMATOGRAFIA</h2>
          <div className="text-sm text-center mt-1 opacity-90">
            Histórico das cromatografias do Campo de Atalaia
          </div>
        </div>

        {/* Tabela Principal */}
        <div className="overflow-x-auto mb-4">
          <table className="w-full text-xs">
            <thead className="bg-blue-800 text-white">
              <tr>
                <th className="p-2 border border-gray-300 min-w-[100px]">DATA DA COLETA</th>
                <th className="p-2 border border-gray-300 min-w-[100px]">DATA DO RELATÓRIO</th>
                <th className="p-2 border border-gray-300 min-w-[100px]">VALIDAÇÃO</th>
                <th className="p-2 border border-gray-300 min-w-[100px]">BOLETIM</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Metanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Etanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Propanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Isobutanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">n-Butanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Isopenthanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">n-Penthanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Hexanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Heptanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Octanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Nonanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Decanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Undecanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Dodecanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Tridecanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">Tetradecanol</th>
                <th className="p-2 border border-gray-300 min-w-[80px]">TOTAL</th>
                <th className="p-2 border border-gray-300 min-w-[120px]">OBSERVAÇÕES</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={row.id} className="hover:bg-gray-50">
                  <td className="p-1 border border-gray-300">
                    <Input
                      value={row.dataColeta}
                      onChange={(e) => handleCellEdit(rowIndex, 'dataColeta', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                      placeholder="DD/MM/AAAA"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      value={row.dataRelatorio}
                      onChange={(e) => handleCellEdit(rowIndex, 'dataRelatorio', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                      placeholder="DD/MM/AAAA"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      value={row.validacao}
                      onChange={(e) => handleCellEdit(rowIndex, 'validacao', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                      placeholder="DD/MM/AAAA"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      value={row.boletim}
                      onChange={(e) => handleCellEdit(rowIndex, 'boletim', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300 bg-green-100">
                    <span className="text-xs">{row.resultado.toFixed(3)}</span>
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.etanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'etanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.propanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'propanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.isobutanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'isobutanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.nbutanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'nbutanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.isopenthanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'isopenthanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.penthanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'penthanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.hexanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'hexanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.heptanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'heptanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.octanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'octanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.nonanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'nonanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.decanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'decanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.undecanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'undecanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.dodecanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'dodecanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.tridecanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'tridecanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      type="number"
                      step="0.001"
                      value={row.tetradecanol}
                      onChange={(e) => handleCellEdit(rowIndex, 'tetradecanol', e.target.value)}
                      className="border-0 bg-gray-200 h-8 text-xs"
                    />
                  </td>
                  <td className="p-1 border border-gray-300 bg-green-100">
                    <span className="text-xs">
                      {(100 - (row.etanol + row.propanol + row.isobutanol + row.nbutanol + 
                        row.isopenthanol + row.penthanol + row.hexanol + row.heptanol + 
                        row.octanol + row.nonanol + row.decanol + row.undecanol + 
                        row.dodecanol + row.tridecanol + row.tetradecanol)).toFixed(3)}%
                    </span>
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      className="border-0 bg-gray-200 h-8 text-xs"
                      placeholder="Observações..."
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <Button onClick={addNewRow} variant="outline" className="mb-4">
          Adicionar Nova Análise
        </Button>
        
        {/* Tabela de Estatísticas */}
        <StatisticsTable data={data} />
      </div>
    </Card>
  );
}