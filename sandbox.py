from enum import Enum
import random
import pygame

from action import Action
from machine import Machine

BOARD_WIDTH = 21
BOARD_HEIGHT = 21
BOARD_CENTER = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
CELL_PX = 24

class RGB(Enum):
  YELLOW = (220, 200, 0)
  GREEN = (0, 150, 0)
  RED = (255, 0, 0)
  BLUE = (80, 80, 255)

def random_action():
    random_colour = random.choice(['y','g'])
    random_animal = random.choice(['k', 'e', 'w', 'p'])
    random_tree = random.choice(['gg', 'wa'])
    return Action(random_colour, random_animal, random_tree)

def random_machine():
    states = {
        ('y','k'):random_action(),
        ('g','k'):random_action(),
        ('y','e'):random_action(),
        ('g','e'):random_action(),
        ('y','w'):random_action(),
        ('g','w'):random_action(),
        ('y','p'):random_action(),
    }
    
    print("\nNew Machine___")
    for state, action in states.items():
        print('('+state[0]+','+state[1]+','+str(action)+')')
    print("________________\n")

    random_colour = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    return Machine(BOARD_CENTER[0], BOARD_CENTER[1], states, random_colour)

def draw_square(screen, x, y, colour):
  if isinstance(colour, RGB):
    colour = colour.value
  pygame.draw.rect(screen, colour, (x * CELL_PX, y * CELL_PX, CELL_PX, CELL_PX))

def draw_text(screen, x, y, text, colour):
    font = pygame.font.SysFont("Arial", 24)
    if isinstance(colour, RGB):
      colour = colour.value
    text = font.render(text, True, colour)
    screen.blit(text, (x * CELL_PX + 4, y * CELL_PX))

def print_help():
    print("\n__________________________________")
    print("Press SPACE to add another machine")
    print("Press C to clear the grid")
    print('Press K to remove all machines')
    print("Press + to speed up the game and - to slow it down")
    print("Press h to read this again")
    print("__________________________________\n")
    
def main():
    """The main function of the game"""
    pygame.init()
    pygame.display.set_caption("Langton's Platypus")
    screen = pygame.display.set_mode((BOARD_WIDTH * CELL_PX, BOARD_HEIGHT * CELL_PX))
    clock = pygame.time.Clock()

    grid = [['y' for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
    machines = [random_machine()]

    running = True

    print_help()


    fps = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    machines.append(random_machine())
                elif event.key == pygame.K_c:
                    print("clearing")
                    grid = [['y' for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
                elif event.key == pygame.K_k:
                    machines = []
                elif event.key == pygame.K_EQUALS:
                    fps =  max(int(1.2 * fps), fps + 1)
                elif event.key == pygame.K_MINUS:
                    if fps > 3:
                        fps = min(int(0.8 * fps), fps - 1)
                elif event.key == pygame.K_h:
                    print_help()
        for m in machines:
            alive = m.act(grid)
            if not alive:
                machines.remove(m)

        screen.fill(RGB.YELLOW.value)
        for x, y in [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == 'g']:
            draw_square(screen, x, y, RGB.GREEN)

        for m in machines:
            draw_text(screen, m.x, m.y, m.animal, m.colour)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
