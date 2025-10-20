import pygame
import random
from Button import AAfilledRoundedRect, Button_IMG


pygame.init()
screen = pygame.display.set_mode((1280, 720))
W, H = 1280, 720

icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
pygame.display.set_caption("Chứng minh tình yêu của mình đi mấy ông!")

font = pygame.font.Font("RobotoSlab-VariableFont_wght.ttf", 74)
text = font.render("Bạn thích Mều hay Du?", True, (255, 255, 255))
text_rect = text.get_rect(center=(640, 150))

congratulations_font = pygame.font.Font("RobotoSlab-VariableFont_wght.ttf", 80)
congratulations_text = congratulations_font.render("", True, (255, 255, 255))
congratulations_text_rect = congratulations_text.get_rect(center=(640, 360))

awful_font = pygame.font.Font("RobotoSlab-VariableFont_wght.ttf", 90)
awful_text = awful_font.render("Sự chung thủy của bạn đâu?", True, (255, 70, 70))
awful_text_rect = awful_text.get_rect(center=(640, 360))

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (1280, 720))
background = pygame.transform.gaussian_blur(background, 10)

k_chan = pygame.image.load("k_chan.jpg")
button_k_chan = Button_IMG(310, 450, k_chan, 0.2, 0.02)

du_chama = pygame.image.load("du_chama.jpg")
button_du_chama = Button_IMG(970, 450, du_chama, 0.2, 0.02)

running = True
check = False
kcehc = False
lock = False

check_move_k = False
check_move_du = False

move_speed = 500

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0

cnt = {"k_chan": 0, "du_chama": 0}

pos_k, pos_du = (310, 450), (970, 450)

scale_k = 0.2
scale_du = 0.2

scale_min = [18, 16, 14, 12, 10, 8, 6, 4, 2, 1]
scale_max = [22, 24, 26, 28, 30, 32, 34, 36, 38, 40]


def get_random_positions(size1, size2, width=1280, height=720):
    r1 = size1 // 2
    r2 = size2 // 2

    x1 = random.randint(r1, width - r1)
    y1 = random.randint(r1, height - r1)

    min_distance = r1 + r2

    can_left = x1 - min_distance >= r2
    can_right = x1 + min_distance <= width - r2
    can_top = y1 - min_distance >= r2
    can_bottom = y1 + min_distance <= height - r2

    available_directions = []
    if can_left:
        available_directions.append(0)
    if can_right:
        available_directions.append(1)
    if can_top:
        available_directions.append(2)
    if can_bottom:
        available_directions.append(3)

    if not available_directions:
        available_directions = [0, 1, 2, 3]

    direction = random.choice(available_directions)

    if direction == 0:
        x2 = random.randint(r2, max(r2, x1 - min_distance))
        y2 = random.randint(r2, height - r2)

    elif direction == 1:
        x2 = random.randint(min(x1 + min_distance, width - r2), width - r2)
        y2 = random.randint(r2, height - r2)

    elif direction == 2:
        x2 = random.randint(r2, width - r2)
        y2 = random.randint(r2, max(r2, y1 - min_distance))

    else:
        x2 = random.randint(r2, width - r2)
        y2 = random.randint(min(y1 + min_distance, height - r2), height - r2)

    return (x2, y2), (x1, y1)


def check_overlap_center(pos1, size1, pos2, size2):
    x1, y1 = pos1
    x2, y2 = pos2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    min_dx = (size1 + size2) // 2
    min_dy = (size1 + size2) // 2

    return dx < min_dx and dy < min_dy


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    if button_k_chan.draw(screen) and not lock and not check_move_k:
        cnt["k_chan"] += 1
        if cnt["du_chama"] > 0:
            kcehc = True
        if cnt["k_chan"] == 10:
            check = True
            congratulations_text = congratulations_font.render("Tình yêu của bạn dành cho\n     K Chan thật tuyệt vời!",
                                                               True,
                                                               (255, 255, 255))
            congratulations_text_rect = congratulations_text.get_rect(center=(640, 360))

        scale_k = scale_min[cnt["k_chan"] - 1] / 100
        scale_du = scale_max[cnt["k_chan"] - 1] / 100

        size_k = int(k_chan.get_width() * scale_k)
        size_du = int(du_chama.get_width() * scale_du)

        button_k_chan = Button_IMG(button_k_chan.x, button_k_chan.y, k_chan, scale_k, scale_k * 0.1)
        button_du_chama = Button_IMG(button_du_chama.x, button_du_chama.y, du_chama, scale_du, scale_du * 0.1)

        pos_k, pos_du = get_random_positions(size_k, size_du, W, H)

        check_move_k = True
        check_move_du = True

    if check_move_k:
        current_x_k, current_y_k = button_k_chan.x, button_k_chan.y
        target_x_k, target_y_k = pos_k
        dx_k, dy_k = target_x_k - current_x_k, target_y_k - current_y_k
        distance_k = (dx_k ** 2 + dy_k ** 2) ** 0.5

        if distance_k > 1:
            move_step = move_speed * dt
            if move_step > distance_k:
                move_step = distance_k
                button_k_chan.x = pos_k[0]
                button_k_chan.y = pos_k[1]
                check_move_k = False
            button_k_chan.x += dx_k / distance_k * move_step
            button_k_chan.y += dy_k / distance_k * move_step
            button_k_chan.rect.center = (button_k_chan.x, button_k_chan.y)
        else:
            check_move_k = False
            button_k_chan.x = pos_k[0]
            button_k_chan.y = pos_k[1]

    if button_du_chama.draw(screen) and not lock and not check_move_du:
        cnt["du_chama"] += 1
        if cnt["k_chan"] > 0:
            kcehc = True
        if cnt["du_chama"] == 10:
            check = True
            congratulations_text = congratulations_font.render("Tình yêu của bạn dành cho\n  Du Chama thật tuyệt vời!", True,
                                                               (255, 255, 255))
            congratulations_text_rect = congratulations_text.get_rect(center=(640, 360))

        scale_du = scale_min[cnt["du_chama"] - 1] / 100
        scale_k = scale_max[cnt["du_chama"] - 1] / 100

        size_k = int(k_chan.get_width() * scale_k)
        size_du = int(du_chama.get_width() * scale_du)

        button_k_chan = Button_IMG(pos_k[0], pos_k[1], k_chan, scale_k, scale_k * 0.1)
        button_du_chama = Button_IMG(pos_du[0], pos_du[1], du_chama, scale_du, scale_du * 0.1)

        pos_du, pos_k = get_random_positions(size_du, size_k, W, H)

        check_move_k = True
        check_move_du = True

    if check_move_du:
        current_x_du, current_y_du = button_du_chama.x, button_du_chama.y
        target_x_du, target_y_du = pos_du
        dx_du, dy_du = target_x_du - current_x_du, target_y_du - current_y_du
        distance_du = (dx_du ** 2 + dy_du ** 2) ** 0.5

        if distance_du > 1:
            move_step = move_speed * dt
            if move_step > distance_du:
                move_step = distance_du
                button_du_chama.x = pos_du[0]
                button_du_chama.y = pos_du[1]
                check_move_du = False
            button_du_chama.x += dx_du / distance_du * move_step
            button_du_chama.y += dy_du / distance_du * move_step
            button_du_chama.rect.center = (button_du_chama.x, button_du_chama.y)
        else:
            check_move_du = False
            button_du_chama.x = pos_du[0]
            button_du_chama.y = pos_du[1]

    AAfilledRoundedRect(screen, text_rect.inflate(40, 40), (0, 0, 0, 200), 0.2)
    screen.blit(text, text_rect)

    if check:
        screen.blit(background, (0, 0))

        AAfilledRoundedRect(screen, congratulations_text_rect.inflate(40, 40), (0, 0, 0, 200), 0.2)
        screen.blit(congratulations_text, congratulations_text_rect)
        lock = True

    if kcehc:
        screen.blit(background, (0, 0))

        AAfilledRoundedRect(screen, awful_text_rect.inflate(40, 40), (0, 0, 0, 200), 0.2)
        screen.blit(awful_text, awful_text_rect)
        lock = True

    pygame.display.update()
