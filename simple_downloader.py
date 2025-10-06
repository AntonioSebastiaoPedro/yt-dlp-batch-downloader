#!/usr/bin/env python3
"""
Script simples para download de playlists - versão minimalista
"""

import subprocess
import sys
from pathlib import Path

def download_playlists(urls_file="playlists.txt"):
    """Download simples de playlists"""
    
    # Verificar se arquivo existe
    if not Path(urls_file).exists():
        print(f"❌ Arquivo {urls_file} não encontrado!")
        return
    
    # Ler URLs
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not urls:
        print("❌ Nenhuma URL encontrada!")
        return
    
    print(f"🚀 Iniciando download de {len(urls)} playlists...")
    
    # Download cada playlist
    for i, url in enumerate(urls, 1):
        print(f"\n📋 Playlist {i}/{len(urls)}: {url}")
        
        cmd = [
            'yt-dlp',
            '--format', 'best[height<=1080]',
            '--output', 'downloads/%(uploader)s/%(playlist)s/%(title)s.%(ext)s',
            '--ignore-errors',
            '--no-overwrites',
            url
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Concluído!")
        except subprocess.CalledProcessError:
            print(f"❌ Erro no download - continuando...")
        except KeyboardInterrupt:
            print("\n🛑 Interrompido pelo usuário")
            break
    
    print(f"\n🎉 Processo finalizado!")

if __name__ == "__main__":
    urls_file = sys.argv[1] if len(sys.argv) > 1 else "playlists.txt"
    download_playlists(urls_file)
