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
    def __init__(self):
      self.image = pygame.image.load("small_tennis.png")
      self.image = pygame.transform.scale(self.image, (60,60))
      self.speed = [2,2]
      self.rect = self.image.get_rect()
      self.rect.top = 30
      self.rect.left = 10
      self.alive = True

    def update(self, clock):
      self.move(clock)

    def move(self, clock):
      self.bounce_off_walls()
      self.rect.x += self.speed[0]
      self.rect.y += int(self.speed[1]*math.sin(pygame.time.get_ticks()/500))
    
      

    def bounce_off_walls(self):
      if self.rect.right > WIDTH:
        self.speed[0] = 2
        self.rect.left = 0
        self.rect.top = random.randrange(20, 300)
        
class Text_Image:
  def __init__(self, text, font):
    self.text = text
    self.font = font
    self.img = font.render(text, True, (128,128,128))
    self.rect = self.img.get_rect()
    self.font = font

  def move_rect(self,x,y):
    self.rect.center = (x,y)

  def make_text_white(self):
    self.img = self.font.render(self.text, True, (255,255,255))

def main():
  pygame.init()
  fly = Fly()
  font = pygame.font.SysFont("freesans", 45)
  trail = create_trail_source()
  list_of_letters = create_char_images(trail, font)
  list_of_letters[0].make_text_white()
  clock = pygame.time.Clock()
  
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  spawn_time = 400
  spawn_timer = 0
  cursor_index = 0
  draw_index = 0
  score = 0
  score_display = Text_Image(f"Score: {score}", font)
  score_display.rect.right = 550
  score_display.rect.bottom = 370
  while True:
    fly.update(clock)
    screen.fill(BACKGROUND)
    screen.blit(fly.image, fly.rect)
    for i in range(cursor_index, draw_index):
      letter = list_of_letters[i]
      screen.blit(letter.img, letter.rect)
    screen.blit(score_display.img, score_display.rect)
    pygame.display.flip()
    clock.tick(60)
    spawn_timer += clock.get_time()
    if spawn_timer >= spawn_time:
      spawn_timer = 0
      list_of_letters[draw_index].move_rect(fly.rect.centerx, fly.rect.centery)
      draw_index += 1
      

      for event in pygame.event.get():
         if event.type == pygame.KEYDOWN:
           if event.key == key_bindings[list_of_letters[cursor_index].text]:
             cursor_index += 1
             list_of_letters[cursor_index].make_text_white()
             

  
def create_trail_source():
  #trail = "thisisasentenceforatraiilofflybitstotypeandtrytokillThisisjustasample"
  trail = [x for x in key_bindings.keys()]
  trail_characters = random.choices(trail, k=50)
  return trail_characters

def create_char_images(list_of_chars, font):
  char_images = []
  for char in list_of_chars:
    char_image = Text_Image(char, font)
    char_images.append(char_image)

  return char_images
  

  
    
  

if __name__ == "__main__":
    main()
