import pygame
import random
import math

WIDTH = 800
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
    self.image = pygame.image.load("fly.png")
    self.image = pygame.transform.scale(self.image, (100, 100))
    self.initial_speed_x = 2
    self.speed = [self.initial_speed_x, 2]
    self.rect = self.image.get_rect()
    self.rect.top = 100
    self.rect.right = 0
    self.alive = True
    self.score_display = score_display
  
  def update(self, total_time):
    self.move(total_time)
    
  
  def move(self, total_time):
    self.rect.x += self.speed[0]
    self.rect.y += int(self.speed[1] * math.sin(total_time / 500))

  def check_speed(self, target_speed):
    if self.speed[0] >= target_speed:
      self.speed[0] -= 1
    else:
      self.speed[0] = target_speed

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
    self.speed = [random.randrange(-3, 3), random.randrange(4, 7)]

  def move_rect(self, x, y):
    self.rect.center = (x, y)

  def change_text_color(self, color: (int, int, int)):
    self.img = self.font.render(self.text, True, color)

  def update_text(self, text):
    self.text = text
    self.img = self.font.render(self.text, True, (255, 255, 255))

  def drop(self):
    self.rect.y += self.speed[1]
    self.rect.x += self.speed[0]


class Game_Logic:
  def __init__(self, font):
    self.font = font
    self.game_running = True    
    self.score = 0
    self.score_display = Text_Image(f"Score: {self.score}", font)
    self.setup_score_display()
    self.fly = Fly(self.score_display)

    self.dead_fly_img = pygame.image.load("dead_fly.png")
    self.dead_fly_img = pygame.transform.scale(self.dead_fly_img, (40, 40))
    self.list_of_words = []
    self.list_of_words = create_list_of_words(self.list_of_words)
    self.word_index = 0
    self.list_of_letters = create_char_images(self.list_of_words[self.word_index], font)
    self.list_of_letters[0].change_text_color((255, 255, 255))
    self.letters_to_draw = []
    self.letters_to_drop = []
    self.dead_flies = []
    self.spawn_time = 200
    self.spawn_timer = 0
    self.toggle_time = 300
    self.toggle_timer = 0
    self.spawn_running = False
    self.cursor_index = 0
    self.draw_index_end = 0
    self.base_speed_x = self.fly.initial_speed_x


  def setup_score_display(self):
    self.score_display.rect.right = 550
    self.score_display.rect.bottom = 370
    

  def update(self,dt, total_time):
    self.fly.check_speed(self.base_speed_x)
    self.fly.update(total_time)
    if self.flew_onscreen():
      if self.flew_offscreen():
        self.reset_fly()
        self.update_score(-5)
      if self.spawn_running:
        self.run_spawn_timer(dt)
      else:
        self.run_toggle_timer(dt)
      self.handle_keyboard()

  def draw(self,screen):
    for df in self.dead_flies:
      screen.blit(df[0], df[1])
    for ldraw in self.letters_to_draw:
      screen.blit(ldraw.img, ldraw.rect)
    for ldrop in self.letters_to_drop:
      ldrop.drop()
      screen.blit(ldrop.img, ldrop.rect)
    screen.blit(self.fly.image, self.fly.rect)
    screen.blit(self.score_display.img, self.score_display.rect)

  def flew_onscreen(self):
    if self.fly.rect.left > 0:
      return True
    else:
      return False
    
  
  def reset_timers(self):
    self.spawn_timer = 0
    self.toggle_timer = 0
    self.spawn_running = False  

  def update_score(self, dscore):
    self.score += dscore
    self.score_display.update_text(f"Score: {self.score}")
    if self.score >= 27:
      self.base_speed_x = 5
    elif self.score >= 18:
      self.base_speed_x = 4
    elif self.score >= 9:
      self.base_speed_x = 3
    

  def flew_offscreen(self):
    if self.fly.rect.centerx > WIDTH:
      return True
    else: 
      return False

  def reset_fly(self):
    self.fly = Fly(self.score_display)
    self.cursor_index = 0
    self.draw_index_end = 0
    for lost_letter in self.letters_to_draw:
        self.letters_to_drop.append(lost_letter)
    self.letters_to_draw.clear()
    self.word_index += 1
    self.reset_timers()
    self.list_of_letters = create_char_images(self.list_of_words[self.word_index], self.font)

  def run_spawn_timer(self, dt):
    self.spawn_timer += dt
    if self.spawn_timer >= self.spawn_time:
      if self.draw_index_end == len(self.list_of_letters):
        self.draw_index_end = 0
        self.spawn_running = False
        self.advance_to_next_word()
        
      else:
        self.spawn_timer = 0
        letter = self.list_of_letters[self.draw_index_end]
        self.letters_to_draw.append(letter)
        if len(self.letters_to_draw) == 1:
            self.letters_to_draw[0].change_text_color((255, 255, 255))
        letter.move_rect(self.fly.rect.centerx, self.fly.rect.centery)
        self.draw_index_end += 1

  def run_toggle_timer(self, dt):
    self.toggle_timer += dt
    if self.toggle_timer >= self.toggle_time:
      self.toggle_timer = 0
      self.spawn_running = True

  def advance_to_next_word(self):
    self.word_index += 1
    self.list_of_letters = create_char_images(
    self.list_of_words[self.word_index], self.font)

  def handle_keyboard(self):
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and self.cursor_index < len(self.letters_to_draw):
        if event.key == key_bindings[self.letters_to_draw[self.cursor_index].text]:
          self.hit_correct_key()        
        else:  
          self.hit_wrong_key()

  def hit_correct_key(self):
    self.letters_to_draw[self.cursor_index].update_text(".")
    if self.cursor_index + 1 >= len(self.letters_to_draw):
      self.update_score(3)
      self.add_dead_fly()
      self.reset_fly()
      self.cursor_index = 0
      for letter_to_draw in self.letters_to_draw:
          self.letters_to_drop.append(letter_to_draw)
      self.letters_to_draw.clear()
      self.advance_to_next_word()
    else:
      self.cursor_index += 1
      self.letters_to_draw[self.cursor_index].change_text_color((255, 255, 255))

  def hit_wrong_key(self):
    missed_right_letter = self.letters_to_draw[self.cursor_index]
    missed_right_letter.change_text_color((255, 0, 0))
    missed_right_letter.img = pygame.transform.scale2x(missed_right_letter.img)
    self.fly.speed[0] = 10

  def add_dead_fly(self):
    dead_fly_rect = self.dead_fly_img.get_rect()
    dead_fly_rect.center = self.fly.rect.center
    self.dead_flies.append([self.dead_fly_img, dead_fly_rect])
    
def main():
  pygame.init()
  font = pygame.font.SysFont("freesans", 35)
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  game_logic = Game_Logic(font)
  
  while game_logic.game_running:
    
    clock.tick(60)
    dt = clock.get_time()
    total_time = pygame.time.get_ticks()
    
    game_logic.update(dt, total_time)

    screen.fill(BACKGROUND)
    game_logic.draw(screen)
    pygame.display.flip()


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
      "tired", "sick", "this", "silly", "wild", "difficult", "rigorous",
      'rowdy', "playful", 'macabre', "blue", "vibrant", "bashful",
      "irritated", "thoughtful", "doubtful", "heroic", "unobtrusive",
      "rustic", "python", "powerful", "worrisome", "nurse", "hospital",
      "glucometer", "charger", "charge", "performed", 'instigate',
      'investigate', 'dry', 'replit', 'stretch', 'xylophone', 'salamander',
      'engulf', 'treatise', 'treasure', 'republican', 'democrat', 'typhoon',
      'antagonize', 'software', 'tutorial', 'television', 'movies',
      'streaming', 'services', 'football', 'foreign', 'industry', 'kidney',
      'ultrasound', 'sonic', 'phonics', 'toddler', 'navigate', 'paper',
      'towel', 'drive', 'chair', 'scanner', 'scrubs', 'crazy', 'germs',
      'seasons', 'honestly', 'bake', 'oxygen', 'amphibian', 'notorious',
      'window', 'eventually', 'finally', 'totally', 'indeed', 'cough',
      'sneeze', 'jump', 'biliary', 'colic', 'mask', 'makes', 'takes', 'tape',
      'needle', 'interpreter', 'wheels', 'charcoal', 'printere', 'band',
      'red', 'yellow', 'orange', 'green', 'blue', 'violet', 'magenta',
      'marigold', 'camper', 'dynasty', 'zebra', 'quick', 'brown', 'lazy',
      'unevniable', 'hexagon', 'hexagonal', 'frame', 'double', 'float',
      'list', 'dictionary', 'diatribe'
  ]
  words_to_add = random.choices(possible_words, k=50)
  for word in words_to_add:
      word_list.append(word)
  return word_list


if __name__ == "__main__":
    main()
