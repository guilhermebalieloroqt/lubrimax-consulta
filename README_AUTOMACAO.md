# 🚀 Automação Lubrimax - Instruções de Configuração

## 📋 Visão Geral do Sistema

```
┌─────────────────────────────────┐
│  💻 SEU PC (5h da manhã)       │
│  • Baixa relatório              │
│  • Processa dados               │
│  • Atualiza db.sqlite           │
│  • Push para GitHub             │
└──────────────┬──────────────────┘
               │
               │ git push
               ▼
┌─────────────────────────────────┐
│  🐙 GITHUB                      │
│  • Armazena código              │
└──────────────┬──────────────────┘
               │
               │ auto deploy
               ▼
┌─────────────────────────────────┐
│  ☁️ STREAMLIT CLOUD (GRÁTIS)   │
│  • SSL automático               │
│  • Deploy automático            │
│  • Atualiza quando GitHub muda │
└──────────────┬──────────────────┘
               │
               │ iframe
               ▼
┌─────────────────────────────────┐
│  🌐 WORDPRESS                   │
│  [consulta_placa]               │
└─────────────────────────────────┘
```

## 📁 Arquivos Criados

### 1. `atualizar_database.py`
Script que processa o Excel e atualiza o banco SQLite.

**Funções principais:**
- `criar_tabela_vendas()` - Cria tabela se não existir
- `limpar_tabela_vendas()` - Remove dados antigos
- `processar_excel()` - Lê e limpa dados do Excel
- `atualizar_database()` - Insere dados no SQLite
- `verificar_dados()` - Mostra estatísticas

### 2. `automacao_completa.py`
Script principal que orquestra todo o processo.

**Fluxo de execução:**
1. Download dos relatórios (Lubrimax + ADJ)
2. Atualização do banco de dados
3. Git commit e push automático
4. Logs detalhados

### 3. `executar_automacao.bat`
Arquivo batch para execução via Agendador de Tarefas.

## ⚙️ Configuração do Agendador de Tarefas do Windows

### Passo 1: Abrir Agendador de Tarefas
1. Pressione `Win + R`
2. Digite: `taskschd.msc`
3. Pressione Enter

### Passo 2: Criar Nova Tarefa
1. Clique em **"Criar Tarefa Básica"** no painel direito
2. Nome: `Automação Lubrimax`
3. Descrição: `Atualização diária dos dados de vendas às 5h`

### Passo 3: Configurar Gatilho
1. Escolha: **"Diariamente"**
2. Hora: **05:00:00**
3. Recorrência: **Todos os dias**

### Passo 4: Configurar Ação
1. Escolha: **"Iniciar um programa"**
2. Programa/script: 
   ```
   C:\Projetos\Lubrimax\Site_Consulta\executar_automacao.bat
   ```
3. Iniciar em: 
   ```
   C:\Projetos\Lubrimax
   ```

### Passo 5: Configurações Avançadas
1. Marque: ✅ **"Executar se o computador estiver ligado ou não"**
2. Marque: ✅ **"Acordar o computador para executar esta tarefa"**
3. Marque: ✅ **"Executar com privilégios mais altos"**

## 🔧 Configuração do Git

### Configurar credenciais do Git (necessário para push automático)

#### Opção 1: Git Credential Manager (Recomendado)
```powershell
git config --global credential.helper manager-core
```
Faça um push manual uma vez para salvar as credenciais.

#### Opção 2: Token de Acesso Pessoal (PAT)
1. Acesse: https://github.com/settings/tokens
2. Gere um novo token com permissão de `repo`
3. Configure:
```powershell
git config --global credential.helper store
git push  # Digite username e o TOKEN como senha
```

### Configurar repositório
```powershell
cd C:\Projetos\Lubrimax
git init
git remote add origin https://github.com/SEU_USUARIO/lubrimax.git
git branch -M main
```

## 📊 Estrutura do Banco de Dados

### Tabela: `vendas`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | ID único (auto-incremento) |
| data_emissao | TEXT | Data da emissão da NF |
| numero_nf | TEXT | Número da nota fiscal |
| cliente | TEXT | Nome do cliente |
| placa | TEXT | Placa do veículo |
| produto | TEXT | Nome do produto |
| quantidade | REAL | Quantidade vendida |
| valor_unitario | REAL | Valor unitário |
| valor_total | REAL | Valor total |
| empresa | TEXT | Lubrimax ou ADJ |
| data_atualizacao | TEXT | Data/hora da atualização |

### Índice
- `idx_placa` na coluna `placa` para buscas rápidas

## 🧪 Testes

### Testar apenas o download:
```powershell
cd C:\Projetos\Lubrimax
python Site_Consulta\download_relatorio.py
```

### Testar apenas a atualização do banco:
```powershell
cd C:\Projetos\Lubrimax
python Site_Consulta\atualizar_database.py
```

### Testar automação completa:
```powershell
cd C:\Projetos\Lubrimax
python Site_Consulta\automacao_completa.py
```

### Testar via arquivo .bat:
```powershell
cd C:\Projetos\Lubrimax\Site_Consulta
executar_automacao.bat
```

## 📝 Logs

Todos os logs são salvos em:
```
C:\Projetos\Lubrimax\Site_Consulta\logs\
├── lubrimax_scraper.log        # Logs do download
├── database_update.log          # Logs da atualização do banco
└── automacao_completa.log       # Logs da automação completa
```

## 🔍 Verificação Manual do Banco

```powershell
cd C:\Projetos\Lubrimax\Site_Consulta
python -c "import sqlite3; conn = sqlite3.connect('data/db.sqlite'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM vendas'); print(f'Total de registros: {cursor.fetchone()[0]}'); cursor.execute('SELECT COUNT(DISTINCT placa) FROM vendas'); print(f'Total de placas únicas: {cursor.fetchone()[0]}'); conn.close()"
```

## 🌐 Configuração do Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Conecte sua conta GitHub
3. Escolha o repositório `lubrimax`
4. Branch: `main`
5. Arquivo principal: `Site_Consulta/app.py`
6. Deploy!

O Streamlit detecta automaticamente mudanças no repositório e faz redeploy.

## 📱 Integração com WordPress

### Shortcode para incorporar:
```html
[consulta_placa url="https://seu-app.streamlit.app"]
```

### Ou via iframe:
```html
<iframe src="https://seu-app.streamlit.app" width="100%" height="600px" frameborder="0"></iframe>
```

## ⚠️ Requisitos

### Python Packages:
```
selenium
pandas
openpyxl
pyautogui
pyperclip
streamlit
```

### Instalar:
```powershell
pip install selenium pandas openpyxl pyautogui pyperclip streamlit
```

## 🆘 Troubleshooting

### Problema: Git push falha
**Solução:** Configure credenciais do Git conforme seção "Configuração do Git"

### Problema: PyAutoGUI não encontra imagem
**Solução:** Verifique a resolução da tela e recapture a imagem do iAdmin

### Problema: Banco não atualiza
**Solução:** Verifique se o Excel foi gerado corretamente em `C:\Projetos\Lubrimax\Vendas_Lubrimax.xlsx`

### Problema: Tarefa agendada não executa
**Solução:** 
- Verifique se o computador está ligado às 5h
- Habilite "Acordar o computador"
- Execute com privilégios de administrador

## 📞 Manutenção

### Verificar última execução:
1. Abrir Agendador de Tarefas
2. Localizar "Automação Lubrimax"
3. Verificar aba "Histórico"

### Forçar execução manual:
1. Clicar com botão direito na tarefa
2. Selecionar "Executar"

## 🎯 Checklist de Implementação

- [ ] Instalar dependências Python
- [ ] Configurar credenciais do Git
- [ ] Criar tarefa no Agendador do Windows
- [ ] Testar execução manual completa
- [ ] Criar repositório no GitHub
- [ ] Configurar Streamlit Cloud
- [ ] Integrar com WordPress
- [ ] Verificar primeiro agendamento (5h da manhã)

---

**🎉 Pronto! O sistema está configurado para rodar automaticamente todos os dias às 5h da manhã!**
