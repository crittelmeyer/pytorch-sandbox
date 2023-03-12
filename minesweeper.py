import pygame
import random

class Minesweeper:
  def __init__(self, width=10, height=10, mines=10, cell_size=40):
    self.width = width
    self.height = height
    self.mines = mines
    self.cell_size = cell_size
    self.board = self.create_board()
    self.hidden_board = self.create_hidden_board()
    self.game_over = False

  def create_board(self):
    board = [[0 for _ in range(self.width)] for _ in range(self.height)]
    for _ in range(self.mines):
      x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
      while board[y][x] == "*":
        x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
      board[y][x] = "*"
      for dy in range(-1, 2):
        for dx in range(-1, 2):
          if not (dx == 0 and dy == 0) and 0 <= x + dx < self.width and 0 <= y + dy < self.height and board[y + dy][x + dx] != "*":
            board[y + dy][x + dx] += 1
    return board

  def create_hidden_board(self):
    return [[False] * self.width for _ in range(self.height)]

  def reveal(self, screen, x, y):
    # Only reveal cells that haven't been revealed yet and that are not mines
    if not self.game_over and not self.hidden_board[y][x]:
      self.hidden_board[y][x] = True
      # If the cell is empty, reveal all neighboring cells recursively
      if self.board[y][x] == 0:
        for dy in range(-1, 2):
          for dx in range(-1, 2):
            # Only reveal cells that are within the board boundaries and haven't been revealed yet
            if not (dx == 0 and dy == 0) and 0 <= x + dx < self.width and 0 <= y + dy < self.height:
              self.reveal(screen, x + dx, y + dy)
        # Change the color of the revealed cell to a light gray
        pygame.draw.rect(screen, (224, 224, 224), pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
      # If the cell is a mine, the game is over
      if self.board[y][x] == "*":
        self.game_over = True
      # If all non-mine cells have been revealed, the game is over
      elif all(all(row) for row in self.hidden_board):
        self.game_over = True



  def draw_board(self, screen):
    for y in range(self.height):
      for x in range(self.width):
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, (192, 192, 192), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Add border around cell
        if self.hidden_board[y][x]:
          if self.board[y][x] == "*":
            pygame.draw.circle(screen, (255, 0, 0), rect.center, self.cell_size // 2 - 5)
          elif self.board[y][x] > 0:
            font = pygame.font.Font(None, self.cell_size - 10)
            text = font.render(str(self.board[y][x]), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


  def get_cell_from_pos(self, pos):
    x, y = pos
    return x // self.cell_size, y // self.cell_size

  def handle_events(self, screen):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          x, y = self.get_cell_from_pos(event.pos)
          self.reveal(screen, x, y)
        elif event.button == 3:
          pass # TODO Implement flagging cells
                
  def run(self):
    pygame.init()
    screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
    clock = pygame.time.Clock()

    while True:
      self.handle_events(screen)

      screen.fill((255, 255, 255))
      self.draw_board(screen)
      pygame.display.flip()

      if self.game_over:
        pygame.time.wait(2000)
        self.__init__(self.width, self.height, self.mines, self.cell_size)

      clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
  game = Minesweeper()
  game.run()