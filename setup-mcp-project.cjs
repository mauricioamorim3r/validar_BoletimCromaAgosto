#!/usr/bin/env node
/**
 * 🚀 MCP SETUP UNIVERSAL - QUALQUER PROJETO VS CODE
 * Detecta tipo de projeto e configura MCPs automaticamente
 * 
 * Uso: node setup-mcp-project.cjs
 * 
 * Este script:
 * 1. Detecta automaticamente o tipo de projeto
 * 2. Gera configuração local específica
 * 3. Cria templates para Claude Desktop
 * 4. Configura deploy automático
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// 🎯 DETECTAR TIPO DE PROJETO
function detectProjectType() {
    console.log('🔍 Detectando tipo de projeto...');
    
    // Python
    if (fs.existsSync('requirements.txt') || fs.existsSync('app.py') || fs.existsSync('main.py')) {
        if (fs.existsSync('render.yaml') || fs.existsSync('gunicorn.conf.py')) {
            return 'python-render-ready';
        }
        return 'python';
    }
    
    // Node.js/JavaScript
    if (fs.existsSync('package.json')) {
        const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
        
        if (pkg.dependencies?.react || pkg.devDependencies?.react) {
            return 'react';
        }
        if (pkg.dependencies?.next || pkg.devDependencies?.next) {
            return 'nextjs';
        }
        if (pkg.dependencies?.express) {
            return 'express';
        }
        if (pkg.dependencies?.vue || pkg.devDependencies?.vue) {
            return 'vue';
        }
        return 'node';
    }
    
    // Go
    if (fs.existsSync('go.mod') || fs.existsSync('main.go')) {
        return 'go';
    }
    
    // Rust
    if (fs.existsSync('Cargo.toml')) {
        return 'rust';
    }
    
    // PHP
    if (fs.existsSync('composer.json') || fs.existsSync('index.php')) {
        return 'php';
    }
    
    return 'generic';
}

// 📋 CONFIGURAÇÕES POR TIPO DE PROJETO  
const PROJECT_CONFIGS = {
    'python-render-ready': {
        buildCommand: "pip install -r requirements.txt",
        startCommand: "gunicorn --config gunicorn.conf.py app:app",
        runtime: "python",
        version: "3.11.7",
        files: ["requirements.txt", "app.py", "runtime.txt", "render.yaml", "gunicorn.conf.py"],
        envVars: {
            "SECRET_KEY": "your_secret_key_here",
            "FLASK_ENV": "production",
            "DEBUG": "false"
        },
        description: "Projeto Python com Flask pronto para Render"
    },
    python: {
        buildCommand: "pip install -r requirements.txt",
        startCommand: "python app.py",
        runtime: "python", 
        version: "3.11.7",
        files: ["requirements.txt", "app.py"],
        envVars: {
            "PYTHONPATH": ".",
            "FLASK_ENV": "production"
        },
        description: "Projeto Python padrão"
    },
    react: {
        buildCommand: "npm install && npm run build",
        startCommand: "npx serve -s build -l $PORT",
        runtime: "static",
        version: "18",
        files: ["package.json", "package-lock.json", "public/", "src/"],
        envVars: {
            "NODE_ENV": "production",
            "GENERATE_SOURCEMAP": "false"
        },
        description: "Aplicação React SPA"
    },
    nextjs: {
        buildCommand: "npm install && npm run build",
        startCommand: "npm start",
        runtime: "node",
        version: "18",
        files: ["package.json", "next.config.js", "pages/", "app/"],
        envVars: {
            "NODE_ENV": "production"
        },
        description: "Aplicação Next.js"
    },
    express: {
        buildCommand: "npm install",
        startCommand: "npm start",
        runtime: "node",
        version: "18",
        files: ["package.json", "server.js", "app.js"],
        envVars: {
            "NODE_ENV": "production"
        },
        description: "API Node.js com Express"
    },
    vue: {
        buildCommand: "npm install && npm run build",
        startCommand: "npx serve -s dist -l $PORT",
        runtime: "static",  
        version: "18",
        files: ["package.json", "vue.config.js", "src/"],
        envVars: {
            "NODE_ENV": "production"
        },
        description: "Aplicação Vue.js"
    },
    node: {
        buildCommand: "npm install",
        startCommand: "node index.js",
        runtime: "node",
        version: "18", 
        files: ["package.json", "index.js"],
        envVars: {
            "NODE_ENV": "production"
        },
        description: "Projeto Node.js genérico"
    },
    go: {
        buildCommand: "go build -o main .",
        startCommand: "./main",
        runtime: "go",
        version: "1.21",
        files: ["go.mod", "main.go"],
        envVars: {
            "GO_ENV": "production"
        },
        description: "Aplicação Go"
    },
    generic: {
        buildCommand: "echo 'No build needed'",
        startCommand: "echo 'Configure start command'",
        runtime: "docker",
        version: "latest",
        files: ["README.md"],
        envVars: {},
        description: "Projeto genérico"
    }
};

// 🔧 GERAR CONFIGURAÇÃO MCP
function generateMCPConfig() {
    const renderKey = process.env.RENDER_API_KEY || "rnd_YOUR_RENDER_KEY_HERE";
    const neonKey = process.env.NEON_API_KEY || "neon_YOUR_NEON_KEY_HERE";
    const githubToken = process.env.GITHUB_TOKEN || "ghp_YOUR_GITHUB_TOKEN";
    
    return {
        "mcpServers": {
            "render": {
                "command": "npx",
                "args": ["-y", "@render/mcp-server"],
                "env": {
                    "RENDER_API_KEY": renderKey
                }
            },
            "neon": {
                "command": "npx",
                "args": ["-y", "@neon/mcp-server"],
                "env": {
                    "NEON_API_KEY": neonKey
                }
            },
            "github": {
                "command": "npx", 
                "args": ["-y", "@github/mcp-server"],
                "env": {
                    "GITHUB_TOKEN": githubToken
                }
            }
        }
    };
}

// 📄 GERAR RENDER.YAML
function generateRenderYaml(config, projectName) {
    return `services:
  - type: web
    name: ${projectName}
    runtime: ${config.runtime}
    buildCommand: ${config.buildCommand}
    startCommand: ${config.startCommand}
    envVars:
${Object.entries(config.envVars).map(([key, value]) => 
      `      - key: ${key}
        value: "${value}"`
    ).join('\n')}`;
}

// 📝 VERIFICAR ARQUIVOS NECESSÁRIOS
function checkRequiredFiles(config) {
    console.log('\n📋 Verificando arquivos necessários...');
    
    const missing = [];
    const present = [];
    
    config.files.forEach(file => {
        if (fs.existsSync(file)) {
            const size = fs.statSync(file).size;
            present.push(`✅ ${file} (${size} bytes)`);
        } else {
            missing.push(`❌ ${file}`);
        }
    });
    
    present.forEach(file => console.log(`  ${file}`));
    missing.forEach(file => console.log(`  ${file}`));
    
    return { present, missing };
}

// 🚀 FUNÇÃO PRINCIPAL
function main() {
    console.log('🚀 MCP SETUP UNIVERSAL - CONFIGURANDO PROJETO...\n');
    
    // Detectar tipo
    const projectType = detectProjectType();
    const config = PROJECT_CONFIGS[projectType];
    const projectName = path.basename(process.cwd()).toLowerCase().replace(/[^a-z0-9-]/g, '-');
    
    console.log(`📂 Projeto detectado: ${projectType.toUpperCase()}`);
    console.log(`📝 Descrição: ${config.description}`);
    console.log(`🏷️  Nome do serviço: ${projectName}`);
    
    // Verificar arquivos
    const fileCheck = checkRequiredFiles(config);
    
    // Criar configuração local
    const localConfig = {
        projectName,
        projectType,
        timestamp: new Date().toISOString(),
        ...config,
        mcpEnabled: true,
        fileCheck
    };
    
    fs.writeFileSync('mcp-project-config.json', JSON.stringify(localConfig, null, 2));
    console.log('\n✅ Configuração local criada: mcp-project-config.json');
    
    // Gerar render.yaml se não existir
    if (!fs.existsSync('render.yaml')) {
        const renderYaml = generateRenderYaml(config, projectName);
        fs.writeFileSync('render.yaml', renderYaml);
        console.log('✅ render.yaml criado');
    } else {
        console.log('ℹ️  render.yaml já existe, mantendo atual');
    }
    
    // Gerar runtime.txt para Python
    if (projectType.includes('python') && !fs.existsSync('runtime.txt')) {
        fs.writeFileSync('runtime.txt', `python-${config.version}`);
        console.log('✅ runtime.txt criado');
    }
    
    // Configuração Claude Desktop
    const mcpConfig = generateMCPConfig();
    
    console.log('\n🎯 CONFIGURAÇÃO CLAUDE DESKTOP:');
    console.log('=' * 50);
    console.log('\n📁 CAMINHO DO ARQUIVO:');
    
    if (os.platform() === 'win32') {
        console.log(`%APPDATA%\\Claude\\claude_desktop_config.json`);
    } else if (os.platform() === 'darwin') {
        console.log(`~/Library/Application Support/Claude/claude_desktop_config.json`);
    } else {
        console.log(`~/.config/claude/claude_desktop_config.json`);
    }
    
    console.log('\n📋 CONTEÚDO PARA COLAR:');
    console.log(JSON.stringify(mcpConfig, null, 2));
    
    // Instruções finais
    console.log('\n' + '=' * 60);
    console.log('🎯 PRÓXIMOS PASSOS:');
    console.log('1. 📋 Cole a configuração no arquivo Claude Desktop');
    console.log('2. 🔄 Reinicie Claude Desktop');  
    console.log('3. 🚀 Execute: node deploy-mcp.js (quando criado)');
    console.log('4. 💬 Use comandos naturais no Claude Desktop!');
    
    console.log('\n✨ COMANDOS DISPONÍVEIS NO CLAUDE:');
    console.log('• "List my Render services"');
    console.log('• "Deploy this project to Render"');
    console.log('• "Show Neon databases"');
    console.log('• "Create development branch"');
    console.log('• "Check deployment status"');
    
    if (fileCheck.missing.length > 0) {
        console.log('\n⚠️  ARQUIVOS AUSENTES:');
        fileCheck.missing.forEach(file => console.log(`   ${file}`));
        console.log('   Crie estes arquivos antes do deploy!');
    }
    
    console.log('\n🎉 CONFIGURAÇÃO MCP CONCLUÍDA! 🎉');
    console.log('=' * 60);
}

// 🏃‍♂️ EXECUTAR SE CHAMADO DIRETAMENTE
if (require.main === module) {
    try {
        main();
    } catch (error) {
        console.error('❌ Erro durante setup:', error.message);
        process.exit(1);
    }
}