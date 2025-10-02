#!/usr/bin/env node
/**
 * 🚀 DEPLOY AUTOMÁTICO VIA MCP
 * Deploy qualquer projeto para Render usando MCPs
 * 
 * Uso: node deploy-mcp.js
 * 
 * Este script:
 * 1. Carrega configuração do projeto
 * 2. Verifica arquivos necessários
 * 3. Gera configurações de deploy
 * 4. Faz commit e push para GitHub
 * 5. Fornece instruções para Claude Desktop
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 🔧 CARREGAR CONFIGURAÇÃO DO PROJETO
function loadProjectConfig() {
    if (!fs.existsSync('mcp-project-config.json')) {
        console.log('❌ Configuração não encontrada!');
        console.log('💡 Execute primeiro: node setup-mcp-project.cjs');
        process.exit(1);
    }
    
    try {
        const config = JSON.parse(fs.readFileSync('mcp-project-config.json', 'utf8'));
        console.log(`📂 Projeto: ${config.projectName} (${config.projectType})`);
        return config;
    } catch (error) {
        console.log('❌ Erro ao ler configuração:', error.message);
        process.exit(1);
    }
}

// 📋 VERIFICAR ARQUIVOS DE DEPLOY
function verifyDeployFiles(config) {
    console.log('\n📋 Verificando arquivos para deploy...');
    
    const requiredFiles = config.files || [];
    const missing = [];
    const present = [];
    
    requiredFiles.forEach(file => {
        if (fs.existsSync(file)) {
            const stats = fs.statSync(file);
            present.push({
                file,
                size: stats.size,
                modified: stats.mtime
            });
            console.log(`  ✅ ${file} (${stats.size} bytes)`);
        } else {
            missing.push(file);
            console.log(`  ❌ ${file} - AUSENTE`);
        }
    });
    
    // Verificar arquivos críticos adicionais
    const criticalFiles = ['README.md', '.gitignore'];
    criticalFiles.forEach(file => {
        if (fs.existsSync(file)) {
            console.log(`  ℹ️  ${file} - OK`);
        } else {
            console.log(`  ⚠️  ${file} - Recomendado criar`);
        }
    });
    
    return { present, missing };
}

// 🔨 GERAR ARQUIVOS DE CONFIGURAÇÃO
function generateConfigFiles(config) {
    console.log('\n🔨 Gerando arquivos de configuração...');
    
    // Gerar/atualizar render.yaml
    const renderYaml = `services:
  - type: web
    name: ${config.projectName}
    runtime: ${config.runtime}
    buildCommand: ${config.buildCommand}
    startCommand: ${config.startCommand}
    plan: free
    region: oregon
    envVars:
${Object.entries(config.envVars || {}).map(([key, value]) => 
      `      - key: ${key}
        value: "${value}"`
    ).join('\n')}
    healthCheckPath: /
    autoDeploy: true`;

    fs.writeFileSync('render.yaml', renderYaml);
    console.log('  ✅ render.yaml atualizado');
    
    // Gerar .gitignore se necessário
    if (!fs.existsSync('.gitignore')) {
        const gitignore = `# Dependencies
node_modules/
__pycache__/
*.pyc
.env
.env.local

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Runtime
*.pid
*.seed
*.tmp

# MCP local config (keep mcp-project-config.json)
# mcp-project-config.json`;

        fs.writeFileSync('.gitignore', gitignore);
        console.log('  ✅ .gitignore criado');
    }
    
    // Gerar runtime.txt para Python
    if (config.projectType.includes('python') && !fs.existsSync('runtime.txt')) {
        fs.writeFileSync('runtime.txt', `python-${config.version || '3.11.7'}`);
        console.log('  ✅ runtime.txt criado');
    }
    
    // Gerar package.json básico se for projeto Node sem package.json
    if (config.runtime === 'node' && !fs.existsSync('package.json')) {
        const packageJson = {
            "name": config.projectName,
            "version": "1.0.0",
            "description": `${config.description} - Deployed via MCP`,
            "main": "index.js",
            "scripts": {
                "start": config.startCommand.replace(/^npm\s+/, ''),
                "build": config.buildCommand.includes('build') ? "npm run build" : "echo 'No build step'",
                "dev": "node index.js",
                "deploy": "node deploy-mcp.js"
            },
            "engines": {
                "node": `>=${config.version || '18'}`
            }
        };
        
        fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
        console.log('  ✅ package.json básico criado');
    }
}

// 🐙 OPERAÇÕES GIT
function handleGitOperations(config) {
    console.log('\n🐙 Preparando deploy via Git...');
    
    try {
        // Verificar se é um repositório Git
        execSync('git rev-parse --is-inside-work-tree', { stdio: 'pipe' });
    } catch (error) {
        console.log('  ℹ️  Inicializando repositório Git...');
        execSync('git init');
        console.log('  ✅ Git inicializado');
    }
    
    try {
        // Adicionar arquivos
        execSync('git add .');
        console.log('  ✅ Arquivos adicionados ao staging');
        
        // Commit
        const commitMessage = `Deploy: MCP auto-deploy ${config.projectType} (${new Date().toISOString()})`;
        execSync(`git commit -m "${commitMessage}"`, { stdio: 'pipe' });
        console.log('  ✅ Commit realizado');
        
        // Verificar remote
        try {
            const remoteUrl = execSync('git config --get remote.origin.url', { encoding: 'utf8' }).trim();
            console.log(`  ℹ️  Remote: ${remoteUrl}`);
            
            // Push
            execSync('git push origin main || git push origin master', { stdio: 'pipe' });
            console.log('  ✅ Código enviado para GitHub');
            
            return remoteUrl;
        } catch (remoteError) {
            console.log('  ⚠️  Nenhum remote configurado');
            console.log('  💡 Configure com: git remote add origin https://github.com/user/repo.git');
            return null;
        }
        
    } catch (gitError) {
        if (gitError.message.includes('nothing to commit')) {
            console.log('  ℹ️  Nenhuma alteração para commit');
        } else {
            console.log('  ⚠️  Erro Git:', gitError.message);
        }
        return null;
    }
}

// 📊 GERAR RELATÓRIO DE DEPLOY
function generateDeployReport(config, fileCheck, gitUrl) {
    console.log('\n📊 RELATÓRIO DE DEPLOY:');
    console.log('=' * 50);
    
    console.log(`\n📂 PROJETO: ${config.projectName}`);
    console.log(`🏷️  Tipo: ${config.projectType}`);
    console.log(`⚙️  Runtime: ${config.runtime} ${config.version || ''}`);
    console.log(`📝 Descrição: ${config.description}`);
    
    console.log(`\n🔨 COMANDOS DE BUILD/START:`);
    console.log(`   Build: ${config.buildCommand}`);
    console.log(`   Start: ${config.startCommand}`);
    
    console.log(`\n📋 ARQUIVOS (${fileCheck.present.length}/${fileCheck.present.length + fileCheck.missing.length}):`);
    fileCheck.present.forEach(file => {
        console.log(`   ✅ ${file.file} (${file.size} bytes)`);
    });
    
    if (fileCheck.missing.length > 0) {
        console.log(`\n❌ ARQUIVOS AUSENTES (${fileCheck.missing.length}):`);
        fileCheck.missing.forEach(file => {
            console.log(`   ❌ ${file}`);
        });
    }
    
    if (gitUrl) {
        console.log(`\n🐙 REPOSITÓRIO: ${gitUrl}`);
    }
    
    console.log(`\n🔐 VARIÁVEIS DE AMBIENTE:`);
    Object.entries(config.envVars || {}).forEach(([key, value]) => {
        console.log(`   ${key} = ${value}`);
    });
}

// 🎯 INSTRUÇÕES CLAUDE DESKTOP
function showClaudeInstructions(config, gitUrl) {
    console.log('\n' + '=' * 60);
    console.log('🎯 PRÓXIMOS PASSOS - CLAUDE DESKTOP:');
    console.log('=' * 60);
    
    console.log('\n💬 COMANDOS PARA USAR NO CLAUDE DESKTOP:');
    console.log('   (Certifique-se que os MCPs estão configurados)');
    
    if (gitUrl) {
        const repoName = gitUrl.split('/').pop().replace('.git', '');
        console.log(`\n🚀 DEPLOY AUTOMÁTICO:`);
        console.log(`   "Create Render service from ${repoName}"`);
        console.log(`   "Deploy ${config.projectName} to Render"`);
        console.log(`   "Setup ${config.projectType} project on Render"`);
    }
    
    console.log(`\n📊 MONITORAMENTO:`);
    console.log(`   "List my Render services"`);
    console.log(`   "Show deployment status for ${config.projectName}"`);
    console.log(`   "Check build logs for ${config.projectName}"`);
    console.log(`   "Show service metrics"`);
    
    console.log(`\n🗄️ BANCO DE DADOS (se necessário):`);
    console.log(`   "List my Neon projects"`);
    console.log(`   "Create database for ${config.projectName}"`);
    console.log(`   "Show connection string"`);
    
    console.log(`\n🔧 TROUBLESHOOTING:`);
    console.log(`   "Debug deployment issues for ${config.projectName}"`);
    console.log(`   "Show recent error logs"`);
    console.log(`   "Restart service ${config.projectName}"`);
    
    console.log('\n📋 CONFIGURAÇÃO MANUAL (se preferir):');
    console.log('1. Acesse https://render.com');
    console.log('2. New + → Web Service');
    console.log(`3. Conecte repositório: ${gitUrl || 'seu-repositorio'}`);
    console.log(`4. Nome: ${config.projectName}`);
    console.log(`5. Build: ${config.buildCommand}`);
    console.log(`6. Start: ${config.startCommand}`);
    console.log('7. Adicione variáveis de ambiente listadas acima');
}

// 🚀 FUNÇÃO PRINCIPAL
function main() {
    console.log('🚀 DEPLOY AUTOMÁTICO VIA MCP - INICIANDO...\n');
    
    try {
        // 1. Carregar configuração
        const config = loadProjectConfig();
        
        // 2. Verificar arquivos
        const fileCheck = verifyDeployFiles(config);
        
        if (fileCheck.missing.length > 0) {
            console.log('\n⚠️  ATENÇÃO: Arquivos ausentes detectados!');
            console.log('   O deploy pode falhar sem estes arquivos.');
            console.log('   Continue mesmo assim? (Ctrl+C para cancelar)');
            
            // Aguardar 3 segundos
            console.log('   Continuando em 3 segundos...');
            setTimeout(() => {}, 3000);
        }
        
        // 3. Gerar arquivos de configuração
        generateConfigFiles(config);
        
        // 4. Operações Git
        const gitUrl = handleGitOperations(config);
        
        // 5. Relatório
        generateDeployReport(config, fileCheck, gitUrl);
        
        // 6. Instruções Claude
        showClaudeInstructions(config, gitUrl);
        
        console.log('\n🎉 DEPLOY PREPARADO COM SUCESSO! 🎉');
        console.log('   Use os comandos acima no Claude Desktop para deploy automático!');
        
    } catch (error) {
        console.error('\n❌ ERRO DURANTE DEPLOY:', error.message);
        console.log('\n💡 DICAS:');
        console.log('• Execute primeiro: node setup-mcp-project.cjs');
        console.log('• Verifique se os arquivos necessários existem');
        console.log('• Configure Git remote se necessário');
        process.exit(1);
    }
}

// 🏃‍♂️ EXECUTAR SE CHAMADO DIRETAMENTE
if (require.main === module) {
    main();
}