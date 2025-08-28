import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';

interface ComponentData {
  id: number;
  component: string;
  percentage: number;
  aga8Status: 'VALIDADO' | 'INVALIDADO';
  cepStatus: 'VALIDADO' | 'INVALIDADO';
  aga8LimitInf: number;
  aga8LimitSup: number;
  cepLimitInf: number;
  cepLimitSup: number;
}

interface PropertyData {
  property: string;
  value: number;
  aga8Status: 'VALIDADO' | 'INVALIDADO';
  cepStatus: 'VALIDADO' | 'INVALIDADO';
  aga8LimitInf: number;
  aga8LimitSup: number;
  cepLimitInf: number;
  cepLimitSup: number;
}

export function CromatografiaAnalysisTable() {
  const [componentsData, setComponentsData] = useState<ComponentData[]>([
    { id: 1, component: 'Metano', percentage: 77.795, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: 96.35, cepLimitSup: 99.15 },
    { id: 2, component: 'Etano', percentage: 3.835, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: 0.05, cepLimitSup: 0.16 },
    { id: 3, component: 'Propano', percentage: 3.149, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 12, cepLimitInf: -0.51, cepLimitSup: 1.32 },
    { id: 4, component: 'i-Butano', percentage: 0.456, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 6, cepLimitInf: -0.02, cepLimitSup: 0.04 },
    { id: 5, component: 'n-Butano', percentage: 0.971, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 6, cepLimitInf: -0.07, cepLimitSup: 0.14 },
    { id: 6, component: 'i-Pentano', percentage: 0.387, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 4, cepLimitInf: -0.07, cepLimitSup: 0.12 },
    { id: 7, component: 'n-Pentano', percentage: 0.412, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 4, cepLimitInf: -0.15, cepLimitSup: 0.25 },
    { id: 8, component: 'Hexano', percentage: 0.329, aga8Status: 'VALIDADO', cepStatus: 'VALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: -0.06, cepLimitSup: 0.33 },
    { id: 9, component: 'Heptano', percentage: 0.237, aga8Status: 'VALIDADO', cepStatus: 'VALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: -0.10, cepLimitSup: 0.27 },
    { id: 10, component: 'Octano', percentage: 0.089, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: 0.00, cepLimitSup: 0.04 },
    { id: 11, component: 'Nonano', percentage: 0.020, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: 0.00, cepLimitSup: 0.01 },
    { id: 12, component: 'Decano', percentage: 0.000, aga8Status: 'VALIDADO', cepStatus: 'VALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: 0.00, cepLimitSup: 0.00 },
    { id: 13, component: 'Oxigênio', percentage: 1.284, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 21, cepLimitInf: -0.04, cepLimitSup: 1.41 },
    { id: 14, component: 'Nitrogênio', percentage: 7.010, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: -0.29, cepLimitSup: 1.41 },
    { id: 15, component: 'CO2', percentage: 3.956, aga8Status: 'VALIDADO', cepStatus: 'INVALIDADO', aga8LimitInf: 0, aga8LimitSup: 100, cepLimitInf: 0.69, cepLimitSup: 0.89 }
  ]);

  const [propertiesData, setPropertiesData] = useState<PropertyData[]>([
    { 
      property: 'Fator de compressibilidade\nCondição de Referência (20°C / 1 atm)', 
      value: 0.9972, 
      aga8Status: 'INVALIDADO', 
      cepStatus: 'INVALIDADO',
      aga8LimitInf: 0,
      aga8LimitSup: 0,
      cepLimitInf: 0.99771,
      cepLimitSup: 0.99824
    },
    { 
      property: 'Massa Específica\nCondição de Referência\n(20°C / 1 atm)', 
      value: 0.885, 
      aga8Status: 'INVALIDADO', 
      cepStatus: 'INVALIDADO',
      aga8LimitInf: 0,
      aga8LimitSup: 0,
      cepLimitInf: 0.6659,
      cepLimitSup: 0.7962
    },
    { 
      property: 'Massa Molecular\n(g/mol)', 
      value: 21.2386, 
      aga8Status: 'INVALIDADO', 
      cepStatus: 'INVALIDADO',
      aga8LimitInf: 0,
      aga8LimitSup: 0,
      cepLimitInf: 15.9888,
      cepLimitSup: 17.4312
    }
  ]);

  // Simulação da busca das últimas 8 análises da base de dados
  const [historicalData, setHistoricalData] = useState<ComponentData[][]>([]);

  useEffect(() => {
    // Simular dados históricos das últimas 8 análises
    const mockHistoricalData = Array.from({ length: 8 }, (_, index) => 
      componentsData.map(comp => ({
        ...comp,
        percentage: comp.percentage + (Math.random() - 0.5) * 0.1 // Pequena variação nos dados históricos
      }))
    );
    setHistoricalData(mockHistoricalData);
  }, []);

  const calculateCEPLimits = (componentId: number) => {
    if (historicalData.length === 0) return { lower: 0, upper: 0 };

    // Buscar os valores históricos para este componente
    const historicalValues = historicalData.map(analysis => 
      analysis.find(comp => comp.id === componentId)?.percentage || 0
    );

    // Calcular média e desvio padrão
    const mean = historicalValues.reduce((sum, val) => sum + val, 0) / historicalValues.length;
    const variance = historicalValues.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / historicalValues.length;
    const stdDev = Math.sqrt(variance);

    // Calcular limites de controle (±3σ)
    const lower = Math.max(0, mean - (3 * stdDev));
    const upper = mean + (3 * stdDev);

    return { lower, upper };
  };

  const validateAGA8 = (component: ComponentData): 'VALIDADO' | 'INVALIDADO' => {
    // Validação AGA8 baseada em parâmetros predefinidos
    if (component.percentage >= component.aga8LimitInf && component.percentage <= component.aga8LimitSup) {
      return 'VALIDADO';
    }
    return 'INVALIDADO';
  };

  const validateCEP = (component: ComponentData): 'VALIDADO' | 'INVALIDADO' => {
    // Validação CEP dinâmica baseada nos limites calculados
    const limits = calculateCEPLimits(component.id);
    if (component.percentage >= limits.lower && component.percentage <= limits.upper) {
      return 'VALIDADO';
    }
    return 'INVALIDADO';
  };

  const handlePercentageChange = (id: number, value: string) => {
    const newValue = parseFloat(value) || 0;
    setComponentsData(prev => 
      prev.map(comp => {
        if (comp.id === id) {
          const updatedComp = { ...comp, percentage: newValue };
          updatedComp.aga8Status = validateAGA8(updatedComp);
          updatedComp.cepStatus = validateCEP(updatedComp);
          
          // Atualizar limites CEP dinâmicos
          const cepLimits = calculateCEPLimits(id);
          updatedComp.cepLimitInf = cepLimits.lower;
          updatedComp.cepLimitSup = cepLimits.upper;
          
          return updatedComp;
        }
        return comp;
      })
    );
  };

  const getTotalPercentage = () => {
    return componentsData.reduce((sum, comp) => sum + comp.percentage, 0);
  };

  const getValidationSummary = () => {
    const aga8Valid = componentsData.filter(comp => comp.aga8Status === 'VALIDADO').length;
    const cepValid = componentsData.filter(comp => comp.cepStatus === 'VALIDADO').length;
    const total = componentsData.length;

    return { aga8Valid, cepValid, total };
  };

  const summary = getValidationSummary();

  return (
    <div className="space-y-6">
      {/* Tabela de Componentes */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs border-collapse border border-gray-300">
          <thead className="bg-blue-800 text-white">
            <tr>
              <th className="p-2 border border-gray-300 w-12">Item</th>
              <th className="p-2 border border-gray-300 min-w-[100px]">Componente</th>
              <th className="p-2 border border-gray-300 w-20">% Molar</th>
              <th className="p-2 border border-gray-300 w-24">Status A.G.A 8</th>
              <th className="p-2 border border-gray-300 w-24">Status CEP</th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#90EE90' }}>
                A.G.A 8<br/>Limite<br/>Inferior
              </th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#90EE90' }}>
                A.G.A 8<br/>Limite<br/>Superior
              </th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#FFA500' }}>
                CEP<br/>Limite<br/>Inferior
              </th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#FFA500' }}>
                CEP<br/>Limite<br/>Superior
              </th>
            </tr>
          </thead>
          <tbody>
            {componentsData.map((comp) => (
              <tr key={comp.id} className="hover:bg-gray-50">
                <td className="p-2 border border-gray-300 text-center">{comp.id}</td>
                <td className="p-2 border border-gray-300">{comp.component}</td>
                <td className="p-1 border border-gray-300">
                  <Input
                    type="number"
                    step="0.001"
                    value={comp.percentage}
                    onChange={(e) => handlePercentageChange(comp.id, e.target.value)}
                    className="border-0 bg-gray-200 h-8 text-xs text-center"
                  />
                </td>
                <td className="p-2 border border-gray-300 text-center">
                  <span className={`px-2 py-1 rounded text-white text-xs ${
                    comp.aga8Status === 'VALIDADO' ? 'bg-green-600' : 'bg-red-600'
                  }`}>
                    {comp.aga8Status}
                  </span>
                </td>
                <td className="p-2 border border-gray-300 text-center">
                  <span className={`px-2 py-1 rounded text-white text-xs ${
                    comp.cepStatus === 'VALIDADO' ? 'bg-green-600' : 'bg-red-600'
                  }`}>
                    {comp.cepStatus}
                  </span>
                </td>
                <td className="p-2 border border-gray-300 text-center bg-green-100">
                  {comp.aga8LimitInf}%
                </td>
                <td className="p-2 border border-gray-300 text-center bg-green-100">
                  {comp.aga8LimitSup}%
                </td>
                <td className="p-2 border border-gray-300 text-center bg-orange-100">
                  {calculateCEPLimits(comp.id).lower.toFixed(2)}%
                </td>
                <td className="p-2 border border-gray-300 text-center bg-orange-100">
                  {calculateCEPLimits(comp.id).upper.toFixed(2)}%
                </td>
              </tr>
            ))}
            <tr className="bg-blue-100">
              <td className="p-2 border border-gray-300 text-center"></td>
              <td className="p-2 border border-gray-300">TOTAL</td>
              <td className="p-2 border border-gray-300 text-center">
                {getTotalPercentage().toFixed(3)}%
              </td>
              <td className="p-2 border border-gray-300" colSpan={6}></td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Tabela de Propriedades */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs border-collapse border border-gray-300">
          <thead className="bg-blue-800 text-white">
            <tr>
              <th className="p-2 border border-gray-300 min-w-[200px]">Propriedade</th>
              <th className="p-2 border border-gray-300 w-24">Valor</th>
              <th className="p-2 border border-gray-300 w-24">Status A.G.A 8</th>
              <th className="p-2 border border-gray-300 w-24">Status CEP</th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#90EE90' }}>
                A.G.A 8<br/>Limite<br/>Inferior
              </th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#90EE90' }}>
                A.G.A 8<br/>Limite<br/>Superior
              </th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#FFA500' }}>
                CEP<br/>Limite<br/>Inferior
              </th>
              <th className="p-2 border border-gray-300 w-20" style={{ backgroundColor: '#FFA500' }}>
                CEP<br/>Limite<br/>Superior
              </th>
            </tr>
          </thead>
          <tbody>
            {propertiesData.map((prop, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="p-2 border border-gray-300 whitespace-pre-line">{prop.property}</td>
                <td className="p-2 border border-gray-300 text-center">{prop.value}</td>
                <td className="p-2 border border-gray-300 text-center">
                  <span className={`px-2 py-1 rounded text-white text-xs ${
                    prop.aga8Status === 'VALIDADO' ? 'bg-green-600' : 'bg-red-600'
                  }`}>
                    {prop.aga8Status}
                  </span>
                </td>
                <td className="p-2 border border-gray-300 text-center">
                  <span className={`px-2 py-1 rounded text-white text-xs ${
                    prop.cepStatus === 'VALIDADO' ? 'bg-green-600' : 'bg-red-600'
                  }`}>
                    {prop.cepStatus}
                  </span>
                </td>
                <td className="p-2 border border-gray-300 text-center bg-green-100">
                  {prop.aga8LimitInf > 0 ? prop.aga8LimitInf : '---'}
                </td>
                <td className="p-2 border border-gray-300 text-center bg-green-100">
                  {prop.aga8LimitSup > 0 ? prop.aga8LimitSup : '---'}
                </td>
                <td className="p-2 border border-gray-300 text-center bg-orange-100">
                  {prop.cepLimitInf.toFixed(5)}
                </td>
                <td className="p-2 border border-gray-300 text-center bg-orange-100">
                  {prop.cepLimitSup.toFixed(5)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Resultado da Validação */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-4">
          <h4 className="mb-2 text-blue-900">Resumo AGA8</h4>
          <div className="text-sm">
            <div>Validados: {summary.aga8Valid}/{summary.total}</div>
            <div className={`mt-1 px-2 py-1 rounded text-white text-center ${
              summary.aga8Valid === summary.total ? 'bg-green-500' : 'bg-red-500'
            }`}>
              {summary.aga8Valid === summary.total ? 'APROVADO' : 'REPROVADO'}
            </div>
          </div>
        </Card>

        <Card className="p-4">
          <h4 className="mb-2 text-blue-900">Resumo CEP</h4>
          <div className="text-sm">
            <div>Validados: {summary.cepValid}/{summary.total}</div>
            <div className={`mt-1 px-2 py-1 rounded text-white text-center ${
              summary.cepValid === summary.total ? 'bg-green-500' : 'bg-red-500'
            }`}>
              {summary.cepValid === summary.total ? 'APROVADO' : 'REPROVADO'}
            </div>
          </div>
        </Card>

        <Card className="p-4">
          <h4 className="mb-2 text-blue-900">Status Geral</h4>
          <div className="text-sm">
            <div>Total: {getTotalPercentage().toFixed(2)}%</div>
            <div className={`mt-1 px-2 py-1 rounded text-white text-center ${
              getTotalPercentage() > 99.5 && getTotalPercentage() < 100.5 ? 'bg-green-500' : 'bg-yellow-500'
            }`}>
              {getTotalPercentage() > 99.5 && getTotalPercentage() < 100.5 ? 'BALANÇO OK' : 'VERIFICAR BALANÇO'}
            </div>
          </div>
        </Card>
      </div>

      {/* Botões de Ação */}
      <div className="flex gap-4">
        <Button className="bg-green-600 hover:bg-green-700">
          Aprovar e Salvar no Banco
        </Button>
        <Button variant="outline">
          Recalcular CEP
        </Button>
        <Button variant="outline">
          Buscar Dados Históricos
        </Button>
      </div>
    </div>
  );
}