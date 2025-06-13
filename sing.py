import pygame
import time
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎶 Bloodline Time 🎶")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 50, 50)
PROGRESS_BAR_COLOR = (50, 255, 50)
FLASH_BG = (30, 30, 30)

FONT = pygame.font.SysFont("Arial", 48, bold=True)

pygame.mixer.music.load("DJ BLOODLINE X TRESNO TEKANE MATI X BABY DONT GO MELODY VIRAL TIKTOK FULL SONG MAMAN FVNDY 2025.mp3")

lyrics = []
with open("lirik.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if "|" in line:
            try:
                time_sec, text = line.split("|", 1)
                lyrics.append((int(time_sec), text))
            except ValueError:
                continue

def draw_progress_bar():
    current_time = time.time() - start_time
    if total_duration > 0:
        progress = current_time / total_duration
    else:
        progress = 0
    bar_width = int(WIDTH * progress)
    pygame.draw.rect(screen, PROGRESS_BAR_COLOR, (0, HEIGHT - 20, bar_width, 10))

def fade_in_word(word, highlight=False, flash=False):
    for alpha in range(0, 256, 30):  # Fade in speed
        screen.fill(FLASH_BG if flash else BLACK)
        draw_progress_bar()

        color = HIGHLIGHT if highlight else WHITE
        word_surface = FONT.render(word, True, color)
        word_surface.set_alpha(alpha)
        word_rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(word_surface, word_rect)

        pygame.display.flip()
        pygame.time.delay(20)

total_duration = 180 


pygame.mixer.music.play()
start_time = time.time()

for t, sentence in lyrics:
    delay = t - (time.time() - start_time)
    if delay > 0:
        time.sleep(delay)

    words = sentence.split()
    for i, word in enumerate(words):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        is_last = (i == len(words) - 1)

   
        beat_timestamps = [21, 22, 25, 26, 28, 30, 33]
        is_beat = t in beat_timestamps

        fade_in_word(word, highlight=is_last, flash=is_beat)
        time.sleep(0.1 if is_beat else 0.3)


while pygame.mixer.music.get_busy():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLACK)
    draw_progress_bar()
    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
