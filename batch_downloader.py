#!/usr/bin/env python3
"""
Script para download automático de múltiplas playlists usando yt-dlp
Autor: Criado com Cascade AI
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import argparse

class PlaylistDownloader:
    def __init__(self, urls_file, download_dir="downloads", max_retries=3, retry_delay=30):
        self.urls_file = urls_file
        self.download_dir = Path(download_dir)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Criar diretório de downloads se não existir
        self.download_dir.mkdir(exist_ok=True)
        
        # Configurar logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"download_log_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def read_urls(self):
        """Lê as URLs do arquivo de texto"""
        try:
            with open(self.urls_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            self.logger.info(f"Carregadas {len(urls)} URLs do arquivo {self.urls_file}")
            return urls
        except FileNotFoundError:
            self.logger.error(f"Arquivo {self.urls_file} não encontrado!")
            return []
        except Exception as e:
            self.logger.error(f"Erro ao ler arquivo: {e}")
            return []
    
    def download_playlist(self, url, attempt=1):
        """Download de uma playlist específica"""
        self.logger.info(f"Iniciando download da playlist (tentativa {attempt}/{self.max_retries}): {url}")
        
        # Comando yt-dlp com configurações otimizadas
        cmd = [
            'yt-dlp',
            '--extract-flat', 'false',  # Extrair informações completas
            '--write-info-json',        # Salvar metadados
            '--write-thumbnail',        # Salvar thumbnails
            '--embed-chapters',         # Incorporar capítulos
            '--embed-metadata',         # Incorporar metadados
            '--format', 'best[height<=1080]',  # Máximo 1080p para economizar espaço
            '--output', str(self.download_dir / '%(uploader)s/%(playlist)s/%(title)s.%(ext)s'),
            '--ignore-errors',          # Continuar mesmo com erros em vídeos individuais
            '--no-overwrites',          # Não sobrescrever arquivos existentes
            '--continue',               # Continuar downloads parciais
            '--retries', '5',           # Retry automático do yt-dlp
            '--fragment-retries', '5',  # Retry para fragmentos
            url
        ]
        
        try:
            # Executar comando
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # Timeout de 1 hora por playlist
            )
            
            if result.returncode == 0:
                self.logger.info(f"✅ Playlist baixada com sucesso: {url}")
                return True
            else:
                self.logger.error(f"❌ Erro no download: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"⏰ Timeout no download da playlist: {url}")
            return False
        except Exception as e:
            self.logger.error(f"💥 Erro inesperado: {e}")
            return False
    
    def download_with_retry(self, url):
        """Download com sistema de retry"""
        for attempt in range(1, self.max_retries + 1):
            success = self.download_playlist(url, attempt)
            
            if success:
                return True
            
            if attempt < self.max_retries:
                self.logger.warning(f"🔄 Tentativa {attempt} falhou. Aguardando {self.retry_delay}s antes da próxima tentativa...")
                time.sleep(self.retry_delay)
            else:
                self.logger.error(f"💀 Todas as tentativas falharam para: {url}")
                
        return False
    
    def run(self):
        """Executa o download de todas as playlists"""
        urls = self.read_urls()
        
        if not urls:
            self.logger.error("Nenhuma URL encontrada para processar!")
            return
        
        self.logger.info(f"🚀 Iniciando download de {len(urls)} playlists...")
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"\n📋 Processando playlist {i}/{len(urls)}")
            self.logger.info(f"🔗 URL: {url}")
            
            if self.download_with_retry(url):
                successful += 1
            else:
                failed += 1
            
            # Pequena pausa entre playlists
            if i < len(urls):
                self.logger.info("⏸️  Pausa de 5 segundos antes da próxima playlist...")
                time.sleep(5)
        
        # Relatório final
        self.logger.info(f"\n📊 RELATÓRIO FINAL:")
        self.logger.info(f"✅ Sucessos: {successful}")
        self.logger.info(f"❌ Falhas: {failed}")
        self.logger.info(f"📁 Downloads salvos em: {self.download_dir.absolute()}")

def main():
    parser = argparse.ArgumentParser(description='Download automático de playlists com yt-dlp')
    parser.add_argument('urls_file', nargs='?', default='playlists.txt', 
                       help='Arquivo com URLs das playlists (padrão: playlists.txt)')
    parser.add_argument('--download-dir', '-d', default='downloads',
                       help='Diretório de download (padrão: downloads)')
    parser.add_argument('--max-retries', '-r', type=int, default=3,
                       help='Número máximo de tentativas por playlist (padrão: 3)')
    parser.add_argument('--retry-delay', '-t', type=int, default=30,
                       help='Delay entre tentativas em segundos (padrão: 30)')
    
    args = parser.parse_args()
    
    # Verificar se yt-dlp está instalado
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp não encontrado! Instale com: pip install yt-dlp")
        sys.exit(1)
    
    # Criar e executar downloader
    downloader = PlaylistDownloader(
        urls_file=args.urls_file,
        download_dir=args.download_dir,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay
    )
    
    try:
        downloader.run()
    except KeyboardInterrupt:
        print("\n🛑 Download interrompido pelo usuário")
        sys.exit(0)

if __name__ == "__main__":
    main()
