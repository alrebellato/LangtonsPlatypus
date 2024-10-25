from enum import Enum
import random
import pygame

BOARD_WIDTH = 21
BOARD_HEIGHT = 21
BOARD_CENTER = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
CELL_PX = 24

class RGB(Enum):
  YELLOW = (220, 200, 0)
  GREEN = (0, 150, 0)
  RED = (255, 0, 0)
  BLUE = (80, 80, 255)

# Machines will have a list of state:action pairs.
class Action:
  def __init__(self, colour, animal, tree):
    self.next_colour = colour
    self.next_animal = animal
    self.tree = tree

  def __str__(self):
    return f"{self.next_colour},{self.next_animal},{self.tree}"

def random_action():
    random_colour = random.choice(['y','g'])
    random_animal = random.choice(['k', 'e', 'w', 'p'])
    random_tree = random.choice(['gg', 'wa'])
    return Action(random_colour, random_animal, random_tree)

# Apply rotation to direction based on the tree
def rotate(dir, tree):
    if tree == 'gg':
        return (-dir[1], dir[0])
    else:
        return (dir[1], -dir[0])

class Machine:
    def __init__(self, states, colour=RGB.RED):
        self.x = BOARD_CENTER[0] # All machines start at center.
        self.y = BOARD_CENTER[1]
        self.animal = 'k' # All machines start as kangaroo
        self.colour = colour
        self.dir = (0, -1)
        self.states = states

    # This needs to be adapted for platypus's as initial configuation.
    def act(self, grid):
        """Act according to genetics, current tile colour, and animal."""
        state = (grid[self.x][self.y], self.animal)
        if state in self.states:
            action = self.states[state]
            self.animal = action.next_animal
            grid[self.x][self.y] = action.next_colour
            self.dir = rotate(self.dir, action.tree)
            self.move(grid)
            return True
        else:
            if self.animal == 'p':
                if grid[self.x][self.y] == 'g':
                    print("Green Platypus. Machine terminating")
            return False

    def move(self, grid):
        self.x += self.dir[0]
        self.y += self.dir[1]

        self.x %= len(grid)
        self.y %= len(grid[0])

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
    
    for state, action in states.items():
        print('('+state[0]+','+state[1]+','+str(action)+')')

    random_colour = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    return Machine(states, random_colour)

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

def main():
    """The main function of the game"""
    pygame.init()
    pygame.display.set_caption("Langton's Platypus")
    screen = pygame.display.set_mode((BOARD_WIDTH * CELL_PX, BOARD_HEIGHT * CELL_PX))
    clock = pygame.time.Clock()

    grid = [['y' for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
    machines = [random_machine()]

    running = True

    print("Press SPACE to add another machine")
    print("Press C to clear the grid")
    print('Press K to remove all machines')
    print("Press + to speed up the game and - to slow it down")


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
