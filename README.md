# 🎥 YT-DLP Batch Playlist Downloader

Script Python para download automático de múltiplas playlists usando yt-dlp com sistema de retry e logging detalhado.

## ✨ Funcionalidades

- **Download automático** de múltiplas playlists
- **Sistema de retry** automático em caso de erro
- **Logging detalhado** com arquivos de log
- **Organização automática** dos arquivos por canal/playlist
- **Continuação de downloads** parciais
- **Metadados e thumbnails** incluídos
- **Configurações otimizadas** para qualidade e espaço

## 📋 Pré-requisitos

1. **Python 3.6+** instalado
2. **yt-dlp** instalado:
   ```bash
   pip install yt-dlp
   ```

## 🚀 Como usar

### 1. Preparar arquivo de URLs

Edite o arquivo `playlists.txt` e adicione as URLs das suas playlists:

```
https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Oq8HmPME
https://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v
https://www.youtube.com/playlist?list=PLu0W_9lII9agICnT8t4iYVSZ3eykIAOME
```

**Dicas:**
- Uma URL por linha
- Linhas que começam com `#` são comentários
- Linhas vazias são ignoradas

### 2. Executar o script

```bash
# Uso básico
python batch_downloader.py

# Especificar arquivo de URLs diferente
python batch_downloader.py minhas_playlists.txt

# Personalizar diretório de download
python batch_downloader.py --download-dir /caminho/para/downloads

# Configurar tentativas e delay
python batch_downloader.py --max-retries 5 --retry-delay 60
```

### 3. Opções disponíveis

```bash
python batch_downloader.py --help
```

**Parâmetros:**
- `urls_file`: Arquivo com URLs (padrão: `playlists.txt`)
- `--download-dir, -d`: Diretório de download (padrão: `downloads`)
- `--max-retries, -r`: Máximo de tentativas por playlist (padrão: 3)
- `--retry-delay, -t`: Delay entre tentativas em segundos (padrão: 30)

## 📁 Estrutura dos arquivos

```
yt-dlp-batch-downloader/
├── batch_downloader.py    # Script principal
├── playlists.txt         # URLs das playlists
├── README.md            # Este arquivo
├── downloads/           # Diretório de downloads
│   └── Canal/
│       └── Playlist/
│           ├── video1.mp4
│           ├── video1.info.json
│           └── video1.webp
└── logs/               # Logs de execução
    └── download_log_20231006_220000.log
```

## 🔧 Configurações do yt-dlp

O script usa as seguintes configurações otimizadas:

- **Qualidade**: Máximo 1080p para economizar espaço
- **Organização**: `Canal/Playlist/Video.ext`
- **Metadados**: JSON com informações completas
- **Thumbnails**: Salvos automaticamente
- **Capítulos**: Incorporados quando disponíveis
- **Retry**: 5 tentativas automáticas por vídeo
- **Continuação**: Downloads parciais são retomados

## 📊 Logs e monitoramento

- **Console**: Progresso em tempo real
- **Arquivo de log**: Histórico completo em `logs/`
- **Relatório final**: Estatísticas de sucesso/falha

Exemplo de saída:
```
2023-10-06 22:00:00 - INFO - 🚀 Iniciando download de 3 playlists...
2023-10-06 22:00:01 - INFO - 📋 Processando playlist 1/3
2023-10-06 22:00:01 - INFO - 🔗 URL: https://www.youtube.com/playlist?list=...
2023-10-06 22:05:30 - INFO - ✅ Playlist baixada com sucesso
```

## 🛠️ Solução de problemas

### Erro: "yt-dlp não encontrado"
```bash
pip install yt-dlp
# ou
pip install --upgrade yt-dlp
```

### Downloads muito lentos
- Verifique sua conexão de internet
- Considere usar `--max-retries 1` para pular vídeos problemáticos mais rápido

### Espaço em disco insuficiente
- Use `--format worst` no código para menor qualidade
- Monitore o espaço disponível

### Playlist privada ou removida
- O script continuará com as próximas playlists
- Verifique os logs para detalhes

## 🎯 Exemplos de uso

### Download básico
```bash
python batch_downloader.py
```

### Download com configurações personalizadas
```bash
python batch_downloader.py playlists_musica.txt --download-dir /media/musicas --max-retries 5
```

### Executar em background (Linux/Mac)
```bash
nohup python batch_downloader.py > output.log 2>&1 &
```

## 📝 Notas importantes

- **Direitos autorais**: Respeite os direitos autorais dos conteúdos
- **Uso responsável**: Não sobrecarregue os servidores
- **Espaço em disco**: Monitore o espaço disponível
- **Interrupção**: Use Ctrl+C para parar o script com segurança

## 🤝 Contribuições

Sinta-se à vontade para melhorar o script e compartilhar suas modificações!
