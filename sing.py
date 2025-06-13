import pygame
import time
import sys
import math

# Setup
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎤 Bloodline Time")

# Warna
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 20, 147)
SHADOW = (0, 0, 0)
PROGRESS_GRADIENT = [(0, 255, 0), (255, 255, 0), (255, 0, 0)]
FLASH_COLORS = [(20, 20, 40), (40, 0, 60), (0, 60, 60)]

# Font
FONT = pygame.font.SysFont("Segoe UI", 44, bold=True)

# Background
bg_image = pygame.image.load("background.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Musik
pygame.mixer.music.load("DJ BLOODLINE X TRESNO TEKANE MATI X BABY DONT GO MELODY VIRAL TIKTOK FULL SONG MAMAN FVNDY 2025.mp3")

# Lirik
lyrics = []
with open("lirik.txt", "r", encoding="utf-8") as f:
    for line in f:
        if "|" in line:
            try:
                t, text = line.strip().split("|", 1)
                lyrics.append((int(t), text.strip()))
            except:
                continue

# Durasi lagu dan beat
total_duration = 180
beat_timestamps = [21, 22, 25, 26, 28, 30, 33, 35]

# Progress bar
def draw_progress_bar():
    now = time.time() - start_time
    progress = min(now / total_duration, 1.0)
    bar_width = int(WIDTH * progress)
    for x in range(bar_width):
        ratio = x / WIDTH
        r = int((1 - ratio) * PROGRESS_GRADIENT[0][0] + ratio * PROGRESS_GRADIENT[-1][0])
        g = int((1 - ratio) * PROGRESS_GRADIENT[0][1] + ratio * PROGRESS_GRADIENT[-1][1])
        b = int((1 - ratio) * PROGRESS_GRADIENT[0][2] + ratio * PROGRESS_GRADIENT[-1][2])
        pygame.draw.line(screen, (r, g, b), (x, HEIGHT - 15), (x, HEIGHT - 5))

# Efek ketik + melayang per karakter
def typewriter_lyric(text, flash=False):
    displayed = ""
    for i, char in enumerate(text):
        displayed += char
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Flash background jika beat
        if flash:
            color_index = i % len(FLASH_COLORS)
            screen.fill(FLASH_COLORS[color_index])
        else:
            screen.blit(bg_image, (0, 0))

        draw_progress_bar()

        # Hitung offset Y animasi goyang
        wave_offset = int(math.sin(time.time() * 5) * 6)

        # Shadow
        shadow_surface = FONT.render(displayed, True, SHADOW)
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 + wave_offset + 3))
        screen.blit(shadow_surface, shadow_rect)

        # Teks utama
        text_surface = FONT.render(displayed, True, HIGHLIGHT)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + wave_offset))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.delay(50)  # Waktu antar karakter

# Mulai lagu
pygame.mixer.music.play()
start_time = time.time()

# Main loop
for t, line in lyrics:
    delay = t - (time.time() - start_time)
    if delay > 0:
        time.sleep(delay)

    flash = t in beat_timestamps
    typewriter_lyric(line, flash=flash)
    time.sleep(0.3 if flash else 0.5)

# Selesai
while pygame.mixer.music.get_busy():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(bg_image, (0, 0))
    draw_progress_bar()
    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
