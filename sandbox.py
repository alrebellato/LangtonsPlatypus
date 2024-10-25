import argparse
import random
import pygame

from action import Action
from machine import Machine
from renderer import RGB, Renderer

def random_action():
    random_colour = random.choice(['y','g'])
    random_animal = random.choice(['k', 'e', 'w', 'p'])
    random_tree = random.choice(['gg', 'wa'])
    return Action(random_colour, random_animal, random_tree)

def random_machine(board_width: int):
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
    return Machine(board_width // 2, board_width // 2, states, random_colour)

def print_help():
    print("\n__________________________________")
    print("Press SPACE to add another machine")
    print("Press C to clear the grid")
    print('Press K to remove all machines')
    print("Press + to speed up the game and - to slow it down")
    print("Press h to read this again")
    print("__________________________________\n")
    
def main():
    parser = argparse.ArgumentParser(description="Langton's Platypus Simulation")
    parser.add_argument('--fps', type=int, default=10, help='Frames per second')
    parser.add_argument('--width', type=int, default=21, help='Canvas width in cells')
    parser.add_argument('--cell_size', type=int, default=8, help='Cell size in pixels')
    args = parser.parse_args()

    board_width = args.width
    fps = args.fps
    cell_px = args.cell_size

    renderer = Renderer(cell_px, board_width)

    pygame.init()
    pygame.display.set_caption("Langton's Platypus")
    screen = pygame.display.set_mode((board_width * cell_px, board_width * cell_px))
    clock = pygame.time.Clock()

    grid = [['y' for _ in range(board_width)] for _ in range(board_width)]
    machines = [random_machine(board_width)]

    running = True

    print_help()


    fps = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    machines.append(random_machine(board_width))
                elif event.key == pygame.K_c:
                    print("clearing")
                    grid = [['y' for _ in range(board_width)] for _ in range(board_width)]
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
            renderer.draw_square(screen, x, y, RGB.GREEN)

        for m in machines:
            renderer.draw_text(screen, m.x, m.y, m.animal, m.colour)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    main()
