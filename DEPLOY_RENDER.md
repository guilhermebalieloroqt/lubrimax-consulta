# Configuração para Deploy no Render

## Passos para fazer o deploy:

### 1. Configurações no Render Dashboard

No painel do Render, configure o seguinte:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run app.py --server.port=10000 --server.address=0.0.0.0
```

OU use o script start.sh:
```bash
chmod +x start.sh && ./start.sh
```

### 2. Variáveis de Ambiente

Se necessário, adicione as seguintes variáveis de ambiente no Render:
- `PYTHON_VERSION` = `3.11.0` (ou sua versão preferida)

### 3. Configurações Importantes

- **Environment**: Python
- **Region**: Escolha a mais próxima
- **Branch**: main (ou a branch que você está usando)
- **Auto-Deploy**: Yes (recomendado)

### 4. Arquivos Necessários

Os seguintes arquivos são essenciais para o deploy:
- ✅ `requirements.txt` - Dependências do Python
- ✅ `app.py` - Aplicação Streamlit principal
- ✅ `.streamlit/config.toml` - Configurações do Streamlit
- ✅ `start.sh` - Script de inicialização (opcional)

### 5. Observações

- O Streamlit usa a porta 10000 por padrão no Render
- O modo headless está habilitado
- CORS e proteção XSRF estão desabilitados para funcionamento correto
- O ChromeDriver pode não funcionar no ambiente do Render (limitação de recursos)

### 6. Alternativas para Automação

Como o Render é um ambiente limitado para automação com Selenium/ChromeDriver, considere:
- Usar serviços como Browserless ou ScrapingBee para o Selenium
- Executar a automação localmente e apenas hospedar a consulta no Render
- Usar um VPS com mais recursos para automação completa

## Troubleshooting

**Erro: gunicorn command not found**
- ✅ Resolvido! Streamlit não usa gunicorn. Use o comando correto no Start Command.

**Erro: Port já em uso**
- Certifique-se que está usando `--server.port=10000`

**Erro: ChromeDriver não funciona**
- O Render tem limitações para executar navegadores. Considere as alternativas acima.
