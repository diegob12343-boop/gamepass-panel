# GamePass Panel

Painel web para conceder gamepasses pagas do Roblox via Open Cloud API.

## Arquivos

```
gamepass-panel/
├── server.py          ← Backend Flask (API)
├── requirements.txt   ← Dependências Python
├── Procfile           ← Configuração Render
└── static/
    └── index.html     ← Painel web
```

## Deploy no Render (grátis)

1. Suba esta pasta para um repositório GitHub
2. Acesse render.com → New Web Service → conecte o repositório
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn server:app`
4. Adicione as variáveis de ambiente:
   - `ADMIN_PASSWORD` → sua senha de acesso ao painel
   - `ROBLOX_API_KEY` → sua chave da Open Cloud API do Roblox

## Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `ADMIN_PASSWORD` | Senha do painel (padrão: admin123) |
| `ROBLOX_API_KEY` | Chave da Open Cloud API do Roblox |
| `PORT` | Porta do servidor (Render define automaticamente) |
