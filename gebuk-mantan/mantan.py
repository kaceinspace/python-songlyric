import pygame
import random
import time
import os
import math
import sys

# Init
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("💔 Gebuk Mantan - Bucin No More Game")
font = pygame.font.SysFont("segoeuiemoji", 32)
big_font = pygame.font.SysFont("segoeuiemoji", 48)
clock = pygame.time.Clock()

# Loading resources
hit_sound = pygame.mixer.Sound("hit.wav")
finish_sound = pygame.mixer.Sound("finish.mp3")
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)

heart = pygame.image.load("heart.png").convert_alpha()
heart = pygame.transform.scale(heart, (20, 20))  # ukuran lebih kecil

punch_img = pygame.image.load("punch.png").convert_alpha()
punch_img = pygame.transform.scale(punch_img, (30, 30))

punch_display = False
punch_time = 0

LEADERBOARD_FILE = "leaderboard.txt"
name_input = ""
gender_choice = None
input_active = True
blink = True
blink_timer = 0

# Partikel
particles = []

def draw_text_center(text, y, size=32, color=(0, 0, 0)):
    f = pygame.font.SysFont("segoeuiemoji", size, bold=True)
    txt = f.render(text, True, color)
    rect = txt.get_rect(center=(WIDTH // 2, y))
    screen.blit(txt, rect)

def draw_gradient_background():
    for y in range(HEIGHT):
        r = 255 - y // 3
        g = 222 - y // 5
        b = 235
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def get_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            lines = f.readlines()
            scores = []
            for line in lines:
                try:
                    name, scr = line.strip().split(":")
                    scores.append((name, int(scr)))
                except:
                    continue
            return sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    return []

def bounce_scale(t):
    return 1 + 0.2 * math.sin(t * 10) * math.exp(-t * 5)

# Transisi cinematic
for i in range(0, 255, 10):
    screen.fill((0, 0, 0))
    draw_text_center("💔 Gebuk Mantan 💔", HEIGHT // 2, 60, (255, 255, 255))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(255 - i)
    overlay.fill((255, 222, 235))
    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    time.sleep(0.01)

# Loop: Input Nama & Gender
while input_active:
    draw_gradient_background()

    draw_text_center("Masukkan Namamu:", 140)
    draw_text_center(name_input + ("|" if blink else ""), 190)

    draw_text_center("Pilih Karakter Mantan (1 = Cewek, 2 = Cowok):", 290)
    if gender_choice == "1":
        draw_text_center("💃 Cewek ✅", 340, color=(255, 0, 128))
    elif gender_choice == "2":
        draw_text_center("🕺 Cowok ✅", 340, color=(0, 102, 255))
    else:
        draw_text_center("Belum dipilih", 340, color=(150, 150, 150))

    pygame.display.flip()
    blink_timer += 1
    if blink_timer > 30:
        blink = not blink
        blink_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and name_input and gender_choice:
                input_active = False
            elif event.key == pygame.K_BACKSPACE:
                name_input = name_input[:-1]
            elif event.unicode in ["1", "2"] and name_input:
                gender_choice = event.unicode
            elif event.unicode.isprintable() and not gender_choice:
                name_input += event.unicode

# Loading karakter
img_file = "mantan_cewek.png" if gender_choice == "1" else "mantan_cowok.png"
mantan_img = pygame.image.load(img_file).convert_alpha()
mantan_img = pygame.transform.scale(mantan_img, (100, 100))

mantan_nangis_img = pygame.image.load("mantan_nangis.png").convert_alpha()
mantan_nangis_img = pygame.transform.scale(mantan_nangis_img, (100, 100))

current_img = mantan_img

mantan_pos = [random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)]

# Ganti Cursor
punch_cursor = pygame.transform.scale(punch_img, (50, 50))
punch_rect = punch_cursor.get_rect()
pygame.mouse.set_visible(False)

# Game state
score = 0
time_limit = 30
start_time = time.time()
hit_time = 0

# Main game loop
running = True
punch_display = False
punch_time = 0

while running:
    draw_gradient_background()
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(mantan_pos[0], mantan_pos[1], 100, 100).collidepoint(event.pos):
                score += 1
                hit_sound.play()
                
                current_img = mantan_nangis_img
                
                punch_display = True
                punch_time = now

                for _ in range(10):
                    particles.append([
                        event.pos[0],
                        event.pos[1],
                        random.randint(-3, 3),
                        random.randint(-5, -1),
                        20
                    ])

                mantan_pos = [random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)]

    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        if p[4] <= 0:
            particles.remove(p)
        else:
            screen.blit(heart, (p[0], p[1]))

    t = now - hit_time
    scale = bounce_scale(t) if t < 0.5 else 1
    size = int(100 * scale)
    mantan_scaled = pygame.transform.scale(current_img, (size, size))
    screen.blit(mantan_scaled, (mantan_pos[0], mantan_pos[1]))

    if now - punch_time > 0.3:
        current_img = mantan_img
        punch_display = False
    
    if punch_display:
        screen.blit(punch_img, (mantan_pos[0], mantan_pos[1]))

    elapsed = now - start_time
    remaining = max(0, int(time_limit - elapsed))
    screen.blit(font.render(f"⏱️ Waktu: {remaining}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"💥 Skor: {score}", True, (0, 0, 0)), (10, 50))
    if remaining <= 0:
        finish_sound.play()
        if score >= 35:
            draw_text_center("GAME OVER - BERHASIL 😁", HEIGHT // 2, 40, (0, 255, 0))
        else:
            draw_text_center("GAME OVER - GAGAL 😭", HEIGHT // 2, 40, (255, 0, 0))
        pygame.display.flip()
        time.sleep(2)
        with open(LEADERBOARD_FILE, "a") as f:
            f.write(f"{name_input}:{score}\n")
        running = False

    mouse = pygame.mouse.get_pos()
    screen.blit(punch_cursor, mouse)

    pygame.display.update()
    clock.tick(60)

# LEADERBOARD
screen.fill((10, 10, 30))
draw_text_center("🏆 TOP 5 GEBUK MANTAN 🏆", 80, 38, (255, 255, 255))
top_scores = get_leaderboard()
card_y = 140

for idx, (name, scr) in enumerate(top_scores, start=1):
    card = pygame.Surface((500, 50))
    card.set_alpha(190)
    card.fill((30, 30, 60))
    pygame.draw.rect(card, (255, 255, 255), (0, 0, 500, 50), 2)
    screen.blit(card, (WIDTH // 2 - 250, card_y))
    draw_text_center(f"{idx}. {name} - {scr} poin", card_y + 25, 28, (255, 255, 255))
    card_y += 60

pygame.display.flip()
time.sleep(7)
pygame.quit()
