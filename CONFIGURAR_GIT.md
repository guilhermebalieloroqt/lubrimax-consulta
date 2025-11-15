# 🔐 Guia de Configuração Git para Automação

## ⚠️ IMPORTANTE: Configure antes de agendar a automação!

Para que o `git push` funcione automaticamente **sem pedir senha**, você precisa configurar as credenciais do Git corretamente.

---

## 📋 Passo a Passo

### 1. Verificar Configuração Atual

Abra o PowerShell e execute:

```powershell
cd C:\Projetos\Lubrimax\Site_Consulta
python testar_git_push.py
```

Este script vai verificar se tudo está configurado corretamente.

---

### 2. Configurar Nome e Email (se necessário)

```powershell
git config --global user.name "Guilherme Balielo"
git config --global user.email "guilherme.balielo@roqt.com.br"
```

---

### 3. Configurar Credenciais para Push Automático

Existem 3 opções (escolha uma):

#### **Opção A: Personal Access Token (Recomendado)** 🌟

1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token" > "Generate new token (classic)"
3. Dê um nome: `Lubrimax Automacao`
4. Marque o escopo: `repo` (acesso completo aos repositórios)
5. Clique em "Generate token"
6. **COPIE o token gerado** (você não verá ele novamente!)

7. Configure o remote com o token:

```powershell
cd C:\Projetos\Lubrimax\Site_Consulta

# Remover remote atual
git remote remove origin

# Adicionar remote com token
git remote add origin https://SEU_TOKEN_AQUI@github.com/guilhermebalieloroqt/lubrimax-consulta.git

# Testar
git push origin main
```

**Exemplo:**
```powershell
git remote add origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/guilhermebalieloroqt/lubrimax-consulta.git
```

---

#### **Opção B: Git Credential Manager (Windows)**

Se você usa Windows e já fez login no Git antes:

```powershell
# Verificar se já está configurado
git config --global credential.helper

# Se não aparecer nada, configurar:
git config --global credential.helper manager-core

# Fazer um push manual para salvar credenciais
git push origin main
# (vai abrir janela para fazer login - faça login uma vez)
```

Depois disso, o Windows vai lembrar suas credenciais.

---

#### **Opção C: Credential Helper Store (Menos Seguro)**

```powershell
# Configurar para salvar credenciais em arquivo
git config --global credential.helper store

# Fazer um push manual
git push origin main
# Digite usuário e token/senha - será salvo automaticamente
```

⚠️ **Atenção:** Suas credenciais ficam em texto plano em `~/.git-credentials`

---

### 4. Testar Configuração

Execute o teste completo:

```powershell
python testar_git_push.py
```

Se tudo estiver ✅ verde, você pode agendar a automação!

---

## 🤖 Como Agendar no Windows (Agendador de Tarefas)

### Método 1: Usar o script PowerShell de setup

```powershell
cd C:\Projetos\Lubrimax\Site_Consulta
.\setup_inicial.ps1
```

### Método 2: Manual

1. Abra o **Agendador de Tarefas** do Windows
2. Criar Tarefa Básica
3. Nome: `Lubrimax - Atualização Diária`
4. Gatilho: Diariamente às **5:00 AM**
5. Ação: **Iniciar um programa**
   - Programa: `C:\Projetos\Lubrimax\Site_Consulta\executar_automacao.bat`
   - Argumentos: `agendado`
6. Configurações avançadas:
   - ✅ Executar independente do usuário estar conectado
   - ✅ Executar com privilégios mais altos
   - ✅ Se falhar, tentar novamente a cada: 10 minutos (3 tentativas)

---

## 🧪 Testar Automação Manual

Antes de agendar, teste manualmente:

```powershell
cd C:\Projetos\Lubrimax\Site_Consulta
.\executar_automacao.bat
```

Verifique se:
- ✅ Download funciona
- ✅ Banco de dados é atualizado
- ✅ Git push é executado com sucesso
- ✅ Sem erro de credenciais

---

## 🔍 Logs e Troubleshooting

### Ver logs da última execução:

```powershell
Get-Content C:\Projetos\Lubrimax\Site_Consulta\logs\automacao_completa.log -Tail 50
```

### Problemas Comuns:

#### ❌ "Authentication failed"
- Suas credenciais não estão salvas
- Token/senha está incorreto
- Reconfigure usando Opção A (Personal Access Token)

#### ❌ "Could not resolve host"
- Sem conexão com internet
- Verifique firewall/proxy

#### ❌ "fatal: not a git repository"
- Execute os comandos no diretório correto: `C:\Projetos\Lubrimax\Site_Consulta`

#### ❌ "Permission denied"
- Token sem permissão de `repo`
- Crie novo token com escopo correto

---

## 📞 Suporte

Em caso de problemas:

1. Execute: `python testar_git_push.py` e veja o diagnóstico
2. Verifique o log: `logs\automacao_completa.log`
3. Teste manualmente: `git push origin main`

---

## ✅ Checklist Final

Antes de agendar, confirme:

- [ ] `python testar_git_push.py` retorna tudo verde ✅
- [ ] `.\executar_automacao.bat` funciona sem erros
- [ ] `git push origin main` funciona sem pedir senha
- [ ] Credenciais Git configuradas
- [ ] Personal Access Token criado (se usar Opção A)
- [ ] Logs funcionando em `logs\automacao_completa.log`

**Tudo OK? Pode agendar! 🚀**
