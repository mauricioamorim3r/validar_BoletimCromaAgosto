import React, { useState } from 'react';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Checkbox } from './ui/checkbox';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { CromatografiaAnalysisTable } from './CromatografiaAnalysisTable';

interface ChecklistItem {
  id: number;
  description: string;
  situation: boolean;
  notApplicable: boolean;
  observation: string;
}

export function ValidationReport() {
  const [formData, setFormData] = useState({
    boletim: '',
    cfqAtlantis: '',
    numeroDoc: '0012/2024',
    dataColeta: '',
    dataEmissao: '',
    dataValidacao: '',
    plataforma: 'FPSO ATLANTE',
    sistemaMedicao: 'GÁS COMBUSTÍVEL LP',
    classificacao: 'FISCAL',
    pontoColeta: 'LP FUEL GAS'
  });

  const [checklist, setChecklist] = useState<ChecklistItem[]>([
    { id: 1, description: 'Identificação do boletim de resultados analíticos', situation: false, notApplicable: false, observation: '' },
    { id: 2, description: 'Identificação da amostra', situation: false, notApplicable: false, observation: '' },
    { id: 3, description: 'Descrição da data de amostragem', situation: false, notApplicable: false, observation: '' },
    { id: 4, description: 'Descrição dos dados de recebimento da amostra pelo laboratório', situation: false, notApplicable: false, observation: '' },
    { id: 5, description: 'Descrição da data de realização das análises', situation: false, notApplicable: false, observation: '' },
    { id: 6, description: 'Descrição da data de emissão do BRA', situation: false, notApplicable: false, observation: '' },
    { id: 7, description: 'Identificação do campo produtor ou da instalação', situation: false, notApplicable: false, observation: '' },
    { id: 8, description: 'Identificação do agente regulado', situation: false, notApplicable: false, observation: '' },
    { id: 9, description: 'Identificação do ponto de medição e/ou do ponto quando aplicável', situation: false, notApplicable: false, observation: '' },
    { id: 10, description: 'Resultados das análises e normas ou procedimentos utilizados', situation: false, notApplicable: false, observation: '' },
    { id: 11, description: 'Descrição dos componentes da composição no processo de ponto de amostragem do fluido (pressão e temperatura)', situation: false, notApplicable: false, observation: '' },
    { id: 12, description: 'Identificação do responsável pela amostragem', situation: false, notApplicable: false, observation: '' },
    { id: 13, description: 'Identificação do responsável pela execução com certificação do ensaio e certificação do técnico de laboratório', situation: false, notApplicable: false, observation: '' },
    { id: 14, description: 'Identificação dos equipamentos utilizados para amostragem dos ensaios', situation: false, notApplicable: false, observation: '' },
    { id: 15, description: 'Identificação dos equipamentos utilizados para execução de ensaios', situation: false, notApplicable: false, observation: '' }
  ]);

  const [validationResult, setValidationResult] = useState({
    aprovado: false,
    reprovado: false,
    observation: ''
  });

  const handleFormChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleChecklistChange = (id: number, field: keyof ChecklistItem, value: any) => {
    setChecklist(prev => 
      prev.map(item => 
        item.id === id ? { ...item, [field]: value } : item
      )
    );
  };

  const handleValidationChange = (field: string, value: any) => {
    setValidationResult(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card className="rounded-t-none border-t-0">
      <div className="p-6">
        {/* Cabeçalho do Formulário */}
        <div className="bg-blue-800 text-white p-4 rounded mb-6">
          <h2 className="text-center">RELATÓRIO DE VALIDAÇÃO DE BOLETIM DE ANÁLISES QUÍMICAS</h2>
        </div>

        {/* Seção de Informações Básicas */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="block text-sm mb-1">Nº BOLETIM:</label>
            <Input
              value={formData.boletim}
              onChange={(e) => handleFormChange('boletim', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">CFQ ATLANTIS:</label>
            <Input
              value={formData.cfqAtlantis}
              onChange={(e) => handleFormChange('cfqAtlantis', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Nº DO DOC:</label>
            <Input
              value={formData.numeroDoc}
              onChange={(e) => handleFormChange('numeroDoc', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">DATA:</label>
            <Input
              type="date"
              value={formData.dataValidacao}
              onChange={(e) => handleFormChange('dataValidacao', e.target.value)}
              className="bg-gray-200"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm mb-1">DATA DA COLETA:</label>
            <Input
              type="date"
              value={formData.dataColeta}
              onChange={(e) => handleFormChange('dataColeta', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">DATA DE EMISSÃO:</label>
            <Input
              type="date"
              value={formData.dataEmissao}
              onChange={(e) => handleFormChange('dataEmissao', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">DATA DE VALIDAÇÃO:</label>
            <Input
              type="date"
              value={formData.dataValidacao}
              onChange={(e) => handleFormChange('dataValidacao', e.target.value)}
              className="bg-gray-200"
            />
          </div>
        </div>

        {/* Seção de Informações Técnicas */}
        <div className="bg-blue-800 text-white p-2 mb-4">
          <h3 className="text-center">1) OBJETIVO</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm mb-1">PLATAFORMA:</label>
            <Input
              value={formData.plataforma}
              onChange={(e) => handleFormChange('plataforma', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">SISTEMA DE MEDIÇÃO:</label>
            <Input
              value={formData.sistemaMedicao}
              onChange={(e) => handleFormChange('sistemaMedicao', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">CLASSIFICAÇÃO:</label>
            <Input
              value={formData.classificacao}
              onChange={(e) => handleFormChange('classificacao', e.target.value)}
              className="bg-gray-200"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">PONTO DE COLETA:</label>
            <Input
              value={formData.pontoColeta}
              onChange={(e) => handleFormChange('pontoColeta', e.target.value)}
              className="bg-gray-200"
            />
          </div>
        </div>

        {/* Checklist */}
        <div className="bg-blue-800 text-white p-2 mb-4">
          <h3 className="text-center">2) CHECK LIST</h3>
        </div>

        <div className="overflow-x-auto mb-6">
          <table className="w-full text-sm border-collapse border border-gray-300">
            <thead className="bg-blue-800 text-white">
              <tr>
                <th className="p-2 border border-gray-300 w-16">ITEM</th>
                <th className="p-2 border border-gray-300">DESCRIÇÃO</th>
                <th className="p-2 border border-gray-300 w-24">SITUAÇÃO</th>
                <th className="p-2 border border-gray-300 w-32">NÃO APLICÁVEL</th>
                <th className="p-2 border border-gray-300 w-40">OBSERVAÇÃO</th>
              </tr>
            </thead>
            <tbody>
              {checklist.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="p-2 border border-gray-300 text-center">
                    {item.id}
                  </td>
                  <td className="p-2 border border-gray-300">
                    {item.description}
                  </td>
                  <td className="p-2 border border-gray-300 text-center">
                    <Checkbox
                      checked={item.situation}
                      onCheckedChange={(checked) => 
                        handleChecklistChange(item.id, 'situation', checked)
                      }
                    />
                  </td>
                  <td className="p-2 border border-gray-300 text-center">
                    <Checkbox
                      checked={item.notApplicable}
                      onCheckedChange={(checked) => 
                        handleChecklistChange(item.id, 'notApplicable', checked)
                      }
                    />
                  </td>
                  <td className="p-1 border border-gray-300">
                    <Input
                      value={item.observation}
                      onChange={(e) => 
                        handleChecklistChange(item.id, 'observation', e.target.value)
                      }
                      className="border-0 bg-gray-200 h-8 text-xs"
                      placeholder="Observação..."
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Seção de Análise CEP */}
        <div className="bg-blue-800 text-white p-2 mb-4">
          <h3 className="text-center">3) ANÁLISE CEP</h3>
        </div>

        <CromatografiaAnalysisTable />

        {/* Seção de Validação */}
        <div className="bg-red-600 text-white p-2 mb-4 mt-8">
          <h3 className="text-center">RESULTADO DA VALIDAÇÃO</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Checkbox
                id="aprovado"
                checked={validationResult.aprovado}
                onCheckedChange={(checked) => {
                  handleValidationChange('aprovado', checked);
                  if (checked) handleValidationChange('reprovado', false);
                }}
              />
              <label htmlFor="aprovado" className="bg-green-500 text-white px-3 py-1 rounded">
                APROVADO
              </label>
            </div>
            <div className="flex items-center gap-2">
              <Checkbox
                id="reprovado"
                checked={validationResult.reprovado}
                onCheckedChange={(checked) => {
                  handleValidationChange('reprovado', checked);
                  if (checked) handleValidationChange('aprovado', false);
                }}
              />
              <label htmlFor="reprovado" className="bg-red-500 text-white px-3 py-1 rounded">
                REPROVADO
              </label>
            </div>
          </div>
          <div>
            <label className="block text-sm mb-1">OBSERVAÇÕES:</label>
            <Textarea
              value={validationResult.observation}
              onChange={(e) => handleValidationChange('observation', e.target.value)}
              className="bg-gray-200 h-20"
              placeholder="Observações sobre a validação..."
            />
          </div>
        </div>

        {/* Seção de Responsáveis */}
        <div className="bg-blue-800 text-white p-2 mb-4">
          <h3 className="text-center">RESPONSÁVEIS PELA ANÁLISE CRÍTICA E VALIDAÇÃO DE ANÁLISE</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm mb-1">ANALISTA JÚNIOR:</label>
            <Input className="bg-gray-200" placeholder="Nome do analista..." />
            <Input className="bg-gray-200 mt-2" placeholder="Data de assinatura..." type="date" />
          </div>
          <div>
            <label className="block text-sm mb-1">ANALISTA SÊNIOR:</label>
            <Input className="bg-gray-200" placeholder="Nome do analista..." />
            <Input className="bg-gray-200 mt-2" placeholder="Data de assinatura..." type="date" />
          </div>
          <div>
            <label className="block text-sm mb-1">ANALISTA SÊNIOR:</label>
            <Input className="bg-gray-200" placeholder="Nome do analista..." />
            <Input className="bg-gray-200 mt-2" placeholder="Data de assinatura..." type="date" />
          </div>
        </div>

        <div className="flex gap-4">
          <Button className="bg-blue-600 hover:bg-blue-700">
            Salvar Validação
          </Button>
          <Button variant="outline">
            Limpar Dados
          </Button>
          <Button variant="outline">
            Exportar PDF
          </Button>
        </div>

        {/* Resumo de Status */}
        <div className="mt-6 p-4 bg-gray-100 rounded">
          <h4 className="mb-2">Status da Validação:</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <strong>Itens Aprovados:</strong> {checklist.filter(item => item.situation).length}/{checklist.length}
            </div>
            <div>
              <strong>Não Aplicáveis:</strong> {checklist.filter(item => item.notApplicable).length}
            </div>
            <div>
              <strong>Status Geral:</strong> 
              <span className={`ml-2 px-2 py-1 rounded text-white ${
                validationResult.aprovado ? 'bg-green-500' : 
                validationResult.reprovado ? 'bg-red-500' : 'bg-gray-500'
              }`}>
                {validationResult.aprovado ? 'APROVADO' : 
                 validationResult.reprovado ? 'REPROVADO' : 'PENDENTE'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}