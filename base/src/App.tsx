import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { ValidationReport } from './components/ValidationReport';
import { CromatografiaValidation } from './components/CromatografiaValidation';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="w-full p-4">
        {/* Cabeçalho Principal */}
        <div className="bg-blue-900 text-white p-4 rounded-t-lg">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="bg-yellow-400 text-black px-3 py-1 rounded font-bold">
                BRAVA
              </div>
              <h1 className="text-xl">SISTEMA DE ANÁLISES QUÍMICAS</h1>
            </div>
          </div>
          <div className="text-sm mt-2 opacity-90">
            Campo de Atalaia - Controle de Qualidade
          </div>
        </div>

        {/* Sistema de Abas */}
        <Tabs defaultValue="validation" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-blue-800 rounded-none">
            <TabsTrigger value="validation" className="text-white data-[state=active]:bg-blue-600">
              VALIDAÇÃO
            </TabsTrigger>
            <TabsTrigger value="cromatografia" className="text-white data-[state=active]:bg-blue-600">
              FULL GAS
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="validation" className="mt-0">
            <ValidationReport />
          </TabsContent>
          
          <TabsContent value="cromatografia" className="mt-0">
            <CromatografiaValidation />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}