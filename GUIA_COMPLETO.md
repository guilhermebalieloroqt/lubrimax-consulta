# 🚀 Sistema de Automação Lubrimax - Guia Definitivo

## 📋 Visão Geral

Este sistema automatiza o processo completo de:
1. ✅ **Download** de relatórios de vendas
2. ✅ **Processamento** dos dados
3. ✅ **Atualização** do banco de dados SQLite
4. ✅ **Push automático** para GitHub
5. ✅ **Deploy automático** no Streamlit Cloud

---

## 🎯 Como Funciona

```
5:00 AM - SEU PC
    ↓
📥 Download Relatório (Selenium)
    ↓
🔄 Processar Dados (Pandas)
    ↓
💾 Atualizar Banco (SQLite)
    ↓
📤 Git Push (GitHub)
    ↓
🚀 Auto Deploy (Streamlit Cloud)
    ↓
🌍 Site Atualizado!
```

---

## ⚙️ Configuração Inicial (Apenas 1 vez)

### Passo 1: Instalar Dependências

```powershell
cd C:\Projetos\Lubrimax\Site_Consulta
pip install -r requirements.txt
```

### Passo 2: Testar Git

```powershell
python testar_git_push.py
```

✅ **TUDO DEVE APARECER VERDE!**

Se aparecer erro, veja: [CONFIGURAR_GIT.md](CONFIGURAR_GIT.md)

### Passo 3: Testar Automação Manualmente

```powershell
.\executar_automacao.bat
```

Deve executar sem erros:
- ✅ Download do relatório
- ✅ Atualização do banco
- ✅ Git push bem-sucedido

### Passo 4: Agendar Execução Diária

```powershell
# Execute como Administrador!
python agendar_automacao.py
```

Isso vai criar uma tarefa que executa **TODO DIA às 5:00 AM**.

---

## 🧪 Testando o Sistema

### Teste 1: Verificar Git
```powershell
python testar_git_push.py
```

Deve retornar: `✅ TUDO OK! Git está configurado corretamente.`

### Teste 2: Executar Automação Manual
```powershell
.\executar_automacao.bat
```

Deve concluir com: `AUTOMACAO CONCLUIDA COM SUCESSO`

### Teste 3: Testar Tarefa Agendada
```powershell
schtasks /Run /TN "Lubrimax_Atualizacao_Diaria"
```

---

## 📊 Monitoramento

### Ver Log da Última Execução
```powershell
Get-Content logs\automacao_completa.log -Tail 100
```

### Ver Histórico de Tarefas Agendadas
1. Pressione `Win + R`
2. Digite: `taskschd.msc`
3. Procure: `Lubrimax_Atualizacao_Diaria`
4. Clique direito > Propriedades > Histórico

### Verificar Status no GitHub
```powershell
git log --oneline -10
```

Deve mostrar commits automáticos diários.

---

## 🔧 Comandos Úteis

### Testar Apenas o Download
```powershell
python download_relatorio.py
```

### Testar Apenas o Banco de Dados
```powershell
python atualizar_database.py
```

### Forçar Push Manual
```powershell
git add .
git commit -m "Atualização manual"
git push origin main
```

### Desabilitar Automação
```powershell
schtasks /Change /TN "Lubrimax_Atualizacao_Diaria" /DISABLE
```

### Habilitar Automação
```powershell
schtasks /Change /TN "Lubrimax_Atualizacao_Diaria" /ENABLE
```

### Remover Automação
```powershell
schtasks /Delete /TN "Lubrimax_Atualizacao_Diaria" /F
```

---

## ❌ Solução de Problemas

### Problema: "Authentication failed" no Git Push

**Solução:**
1. Crie um Personal Access Token no GitHub:
   - https://github.com/settings/tokens
   - Gerar token com escopo `repo`
   
2. Configure o remote com token:
```powershell
git remote set-url origin https://SEU_TOKEN@github.com/guilhermebalieloroqt/lubrimax-consulta.git
```

3. Teste:
```powershell
git push origin main
```

Veja guia completo: [CONFIGURAR_GIT.md](CONFIGURAR_GIT.md)

---

### Problema: Selenium não encontra ChromeDriver

**Solução:**
```powershell
# Verificar se existe
dir chromedriver-win64\chromedriver.exe

# Se não existir, baixar:
# https://chromedriver.chromium.org/downloads
```

---

### Problema: Automação não executa no horário

**Solução:**
1. Verifique se a tarefa está ativa:
```powershell
schtasks /Query /TN "Lubrimax_Atualizacao_Diaria"
```

2. PC precisa estar ligado às 5:00 AM
3. Configurar para "acordar PC para executar":
   - Agendador de Tarefas > Propriedades da Tarefa
   - Aba "Condições"
   - ✅ Ativar: "Ativar o computador para executar esta tarefa"

---

### Problema: Banco de dados não atualiza

**Solução:**
```powershell
# Verificar se arquivo existe
dir data\db.sqlite

# Ver tamanho
(Get-Item data\db.sqlite).length

# Testar manualmente
python database.py
```

---

## 📁 Estrutura de Arquivos

```
Site_Consulta/
├── 🤖 automacao_completa.py       # Script principal
├── 📥 download_relatorio.py       # Download dos relatórios
├── 💾 atualizar_database.py       # Atualiza banco de dados
├── 🔍 database.py                 # Consultas ao banco
├── 🎨 app.py                      # Interface Streamlit
├── 🧪 testar_git_push.py         # Teste de configuração Git
├── 📅 agendar_automacao.py       # Cria tarefa agendada
├── 🪟 executar_automacao.bat     # Script Windows
├── 📋 CONFIGURAR_GIT.md          # Guia de configuração Git
└── 📊 logs/
    └── automacao_completa.log    # Logs de execução
```

---

## ✅ Checklist Final

Antes de considerar tudo pronto, confirme:

- [ ] `python testar_git_push.py` ✅ tudo verde
- [ ] `.\executar_automacao.bat` funciona sem erros
- [ ] `git push origin main` funciona sem pedir senha
- [ ] Tarefa agendada criada: `schtasks /Query /TN "Lubrimax_Atualizacao_Diaria"`
- [ ] Log está sendo gerado: `logs\automacao_completa.log`
- [ ] Streamlit app funciona: https://seu-app.streamlit.app

---

## 🆘 Suporte

Se nada funcionar:

1. **Execute o diagnóstico completo:**
```powershell
python testar_git_push.py > diagnostico.txt
Get-Content diagnostico.txt
```

2. **Veja o log:**
```powershell
Get-Content logs\automacao_completa.log -Tail 50
```

3. **Teste cada componente:**
```powershell
# Teste 1: Python
python --version

# Teste 2: Git
git --version
git remote -v

# Teste 3: Download
python download_relatorio.py

# Teste 4: Banco
python -c "import sqlite3; print('SQLite OK')"

# Teste 5: Push
git push origin main
```

---

## 📞 Contato

Em caso de problemas críticos, entre em contato com o desenvolvedor.

---

## 🎉 Pronto!

Se todos os testes passaram, seu sistema está 100% automatizado! 🚀

A automação vai executar **TODO DIA às 5:00 AM** e atualizar os dados automaticamente.

**Relaxe e deixe o robô trabalhar! 🤖**
