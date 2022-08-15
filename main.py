import pygame
import random
import math

WIDTH = 600
HEIGHT = 400
BACKGROUND = (0, 0, 0)
key_bindings = {
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z
}


class Fly:
    def __init__(self, score_display):
        self.image = pygame.image.load("small_tennis.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.speed = [1, 2]
        self.rect = self.image.get_rect()
        self.rect.top = 30
        self.rect.left = 10
        self.alive = True
        self.score_display = score_display

    def update(self, clock):
        self.move(clock)

    def move(self, clock):
        self.bounce_off_walls()
        self.rect.x += self.speed[0]
        self.rect.y += int(self.speed[1] *
                           math.sin(pygame.time.get_ticks() / 500))

    def bounce_off_walls(self):
        if self.rect.right > WIDTH:
            self.reset_to_left_side()

    def reset_to_left_side(self):
        self.rect.left = 0
        self.rect.top = random.randrange(20, 300)


class Text_Image:
    def __init__(self, text, font):
        self.text = text
        self.font = font
        self.img = font.render(text, True, (128, 128, 128))
        self.rect = self.img.get_rect()
        self.font = font

    def move_rect(self, x, y):
        self.rect.center = (x, y)

    def change_text_color(self, color: (int, int, int)):
        self.img = self.font.render(self.text, True, color)

    def update_text(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, (255, 255, 255))


def main():
    pygame.init()
    font = pygame.font.SysFont("freesans", 45)

    score = 0
    score_display = Text_Image(f"Score: {score}", font)
    score_display.rect.right = 550
    score_display.rect.bottom = 370

    fly = Fly(score_display)
    list_of_words = []
    list_of_words = create_list_of_words(list_of_words)
    word_index = 0
    trail = create_trail_source()
    list_of_letters = create_char_images(list_of_words[word_index], font)
    list_of_letters[0].change_text_color((255, 255, 255))
    letters_to_draw = []
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    spawn_time = 300
    spawn_timer = 0
    toggle_time = 750
    toggle_timer = -150
    spawn_running = False
    cursor_index = 0
    draw_index_end = 0

    while True:
        fly.update(clock)
        screen.fill(BACKGROUND)
        screen.blit(fly.image, fly.rect)
        for letter in letters_to_draw:
            screen.blit(letter.img, letter.rect)
        screen.blit(score_display.img, score_display.rect)
        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time()

        if spawn_running:
            spawn_timer += dt
            if spawn_timer >= spawn_time:
                if draw_index_end == len(list_of_letters):
                    draw_index_end = 0
                    spawn_running = False
                    word_index += 1
                    list_of_letters = create_char_images(
                        list_of_words[word_index], font)
                else:
                    spawn_timer = 0
                    letter = list_of_letters[draw_index_end]
                    letters_to_draw.append(letter)
                    letter.move_rect(fly.rect.centerx, fly.rect.centery)
                    draw_index_end += 1

        else:
            toggle_timer += dt
            if toggle_timer >= toggle_time:
                toggle_timer = 0
                spawn_running = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == key_bindings[
                        letters_to_draw[cursor_index].text]:
                    letters_to_draw[cursor_index].update_text(".")
                    cursor_index += 1
                    
                    if cursor_index >= len(letters_to_draw):
                        score += 1
                        score_display.update_text(f"Score: {score}")
                        spawn_timer = 0
                        #draw_index_start = draw_index_end
                        fly.reset_to_left_side()
                    else:
                      letters_to_draw[cursor_index].change_text_color(
                        (255, 255, 255))


def create_trail_source():
    #trail = "thisisasentenceforatraiilofflybitstotypeandtrytokillThisisjustasample"
    trail = [x for x in key_bindings.keys()]
    trail_characters = random.choices(trail, k=100)
    return trail_characters


def create_char_images(list_of_chars, font):
    char_images = []
    for char in list_of_chars:
        char_image = Text_Image(char, font)
        char_images.append(char_image)

    return char_images


def create_list_of_words(word_list):
    possible_words = [
        "test", "bob", "trial", "just", "need", "some", "words", "tiff",
        "foot", "feelings", "kind", "funny", "fly", "alabaster", "strictly",
        "fanciful", "macabre", "happy", "joyful", "exuberant", "angry",
        "tired", "sick of this", "silly", "wild", "difficult", "rigorous",
        'rowdy', "playful", 'macabre', "blue", "vibrant", "bashful",
        "irritated", "thoughtful", "doubtful", "heroic", "unobtrusive",
        "rustic", "python", "powerful", "worrisome", "nurse", "hospital",
        "glucometer", "charger", "charge", "performed"
    ]
    words_to_add = random.choices(possible_words, k=50)
    for word in words_to_add:
        word_list.append(word)
    return word_list


if __name__ == "__main__":
    main()
