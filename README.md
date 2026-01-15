# Travazap Automation Bot

Este é um aplicativo de automação para Ubuntu que interage com o Telegram Web para realizar ações automatizadas no bot "Travazap".

## Funcionalidades

- **Autenticação Automática**: Exibe QR Code no terminal para login.
- **Navegação Inteligente**: Acessa o grupo e navega nos menus.
- **Ciclo de Ações**: Executa comandos de "Crash" ciclicamente.
- **Interface Terminal**: Logs detalhados e contagem regressiva.

## Requisitos

- Ubuntu LTS (ou compatível)
- Python 3.8+
- Bibliotecas do sistema para OpenCV (geralmente já instaladas ou via `apt install libgl1`)

## Instalação

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Se tiver problemas com o `opencv`, instale as dependências do sistema:
   ```bash
   sudo apt-get update && sudo apt-get install -y libgl1
   ```

## Uso

Execute o bot:
```bash
python3 main.py
```

1. O bot iniciará o navegador em modo "headless" (sem interface gráfica).
2. Um QR Code será exibido no terminal.
3. Abra seu Telegram no celular -> Configurações -> Dispositivos -> Conectar Desktop.
4. Escaneie o QR Code do terminal.
5. O bot iniciará a automação automaticamente.

## Parar

Pressione `Ctrl+C` a qualquer momento para parar o bot com segurança.
