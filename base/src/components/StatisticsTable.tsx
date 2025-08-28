import React from 'react';
import { Card } from './ui/card';

interface CromatografiaData {
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

interface StatisticsTableProps {
  data: CromatografiaData[];
}

export function StatisticsTable({ data }: StatisticsTableProps) {
  const calculateStatistics = (field: string) => {
    if (data.length === 0) return { mean: 0, stdDev: 0, min: 0, max: 0 };

    const values = data.map(row => row[field] || 0);
    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);
    const min = Math.min(...values);
    const max = Math.max(...values);

    return { mean, stdDev, min, max };
  };

  const fields = [
    'etanol', 'propanol', 'isobutanol', 'nbutanol', 'isopenthanol',
    'penthanol', 'hexanol', 'heptanol', 'octanol', 'nonanol',
    'decanol', 'undecanol', 'dodecanol', 'tridecanol', 'tetradecanol'
  ];

  const fieldLabels = {
    etanol: 'Etanol',
    propanol: 'Propanol',
    isobutanol: 'Isobutanol',
    nbutanol: 'n-Butanol',
    isopenthanol: 'Isopenthanol',
    penthanol: 'n-Penthanol',
    hexanol: 'Hexanol',
    heptanol: 'Heptanol',
    octanol: 'Octanol',
    nonanol: 'Nonanol',
    decanol: 'Decanol',
    undecanol: 'Undecanol',
    dodecanol: 'Dodecanol',
    tridecanol: 'Tridecanol',
    tetradecanol: 'Tetradecanol'
  };

  return (
    <Card className="mt-6">
      <div className="p-4">
        <h2 className="mb-4 text-blue-900">Controle Estatístico de Processo (CEP)</h2>
        
        <div className="overflow-x-auto">
          <table className="w-full text-xs border-collapse border border-gray-300">
            <thead className="bg-blue-800 text-white">
              <tr>
                <th className="p-2 border border-gray-300 text-left">Componente</th>
                <th className="p-2 border border-gray-300">Média</th>
                <th className="p-2 border border-gray-300">Desvio Padrão</th>
                <th className="p-2 border border-gray-300">Mínimo</th>
                <th className="p-2 border border-gray-300">Máximo</th>
                <th className="p-2 border border-gray-300">LSC (+3σ)</th>
                <th className="p-2 border border-gray-300">LIC (-3σ)</th>
                <th className="p-2 border border-gray-300">Faixa</th>
                <th className="p-2 border border-gray-300">CV%</th>
              </tr>
            </thead>
            <tbody>
              {fields.map((field) => {
                const stats = calculateStatistics(field);
                const lsc = stats.mean + (3 * stats.stdDev);
                const lic = Math.max(0, stats.mean - (3 * stats.stdDev));
                const range = stats.max - stats.min;
                const cv = stats.mean > 0 ? (stats.stdDev / stats.mean) * 100 : 0;

                return (
                  <tr key={field} className="hover:bg-gray-50">
                    <td className="p-2 border border-gray-300 font-medium">
                      {fieldLabels[field as keyof typeof fieldLabels]}
                    </td>
                    <td className="p-2 border border-gray-300 text-center">
                      {stats.mean.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center">
                      {stats.stdDev.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center">
                      {stats.min.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center">
                      {stats.max.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center bg-red-50">
                      {lsc.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center bg-red-50">
                      {lic.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center">
                      {range.toFixed(6)}
                    </td>
                    <td className="p-2 border border-gray-300 text-center">
                      {cv.toFixed(2)}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-4">
            <h3 className="mb-2 text-blue-900">Número de Amostras</h3>
            <div className="text-2xl">{data.length}</div>
          </Card>
          
          <Card className="p-4">
            <h3 className="mb-2 text-blue-900">Última Análise</h3>
            <div className="text-sm">
              {data.length > 0 ? data[data.length - 1].dataColeta || 'Não informado' : 'Nenhuma análise'}
            </div>
          </Card>
          
          <Card className="p-4">
            <h3 className="mb-2 text-blue-900">Status do Processo</h3>
            <div className="text-sm text-green-600">
              {data.length > 5 ? 'Controle Estatístico Ativo' : 'Aguardando mais dados'}
            </div>
          </Card>
        </div>

        <div className="mt-4 text-xs text-gray-600">
          <p><strong>Legendas:</strong></p>
          <p>LSC: Limite Superior de Controle | LIC: Limite Inferior de Controle</p>
          <p>CV: Coeficiente de Variação | σ: Desvio Padrão</p>
        </div>
      </div>
    </Card>
  );
}