import os
import pygame
import wave
import math
import struct
import random

# Configuração: Agora incluímos a pasta "music" explicitamente
FOLDERS = ["images", "sounds", "music"]
pygame.init()

def create_folders():
    for folder in FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Pasta '{folder}' criada/verificada.")

def create_image(name, size, color, detail_color=None):
    """Cria uma imagem simples e salva como PNG"""
    surface = pygame.Surface(size)
    surface.fill(color)
    
    if detail_color:
        pygame.draw.rect(surface, detail_color, (size[0]//4, size[1]//4, size[0]//2, size[1]//2))
    
    path = os.path.join("images", name + ".png")
    pygame.image.save(surface, path)
    print(f"Imagem criada: {path}")

def create_sound_jump(filename):
    """Salva na pasta SOUNDS"""
    path = os.path.join("sounds", filename)
    with wave.open(path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        data = bytearray()
        for i in range(10000): 
            freq = 200 + (i / 50) 
            val = int(32767.0 * math.sin(2 * math.pi * freq * i / 44100))
            data += struct.pack('<h', val)
        wav_file.writeframes(data)
    print(f"Efeito sonoro criado: {path}")

def create_sound_music(filename):
    """Salva na pasta MUSIC (Correção Crítica)"""
    path = os.path.join("music", filename)
    with wave.open(path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        data = bytearray()
        # Melodia simples
        notes = [220, 220, 261, 330, 220, 196] 
        for note in notes:
            for i in range(8000): 
                val = int(10000.0 * math.sin(2 * math.pi * note * i / 44100))
                data += struct.pack('<h', val)
        wav_file.writeframes(data)
    print(f"Música criada: {path}")

def main():
    create_folders()
    
    # --- CRIAÇÃO DE IMAGENS ---
    create_image("hero_idle_1", (32, 32), (0, 0, 200), (0, 0, 255))
    create_image("hero_idle_2", (32, 32), (0, 0, 200), (50, 50, 255))
    create_image("hero_run_1", (32, 32), (0, 0, 200), (0, 255, 255))
    create_image("hero_run_2", (32, 32), (0, 0, 200), (255, 255, 0))
    
    create_image("hero_idle_1_left", (32, 32), (0, 0, 200), (0, 0, 255))
    create_image("hero_idle_2_left", (32, 32), (0, 0, 200), (50, 50, 255))
    create_image("hero_run_1_left", (32, 32), (0, 0, 200), (0, 255, 255))
    create_image("hero_run_2_left", (32, 32), (0, 0, 200), (255, 255, 0))

    create_image("enemy_1", (30, 30), (200, 0, 0), (255, 100, 100))
    create_image("enemy_2", (30, 30), (200, 0, 0), (100, 0, 0))
    
    create_image("block", (50, 50), (100, 255, 100), (139, 69, 19))
    
    create_image("btn_start", (200, 50), (100, 100, 100), (0, 255, 0))
    create_image("btn_sound", (200, 50), (100, 100, 100), (0, 0, 255)) 
    create_image("btn_exit", (200, 50), (100, 100, 100), (255, 0, 0)) 

    # --- CRIAÇÃO DE SONS ---
    create_sound_jump("jump.wav")   # Vai para /sounds
    create_sound_music("music.wav") # Vai para /music (CORRIGIDO)

    print("\nSUCESSO! Estrutura corrigida.")
    print("Agora execute: pgzrun game.py")

if __name__ == "__main__":
    main()
