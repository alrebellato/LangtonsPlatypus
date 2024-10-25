class Machine:
    def __init__(self, x, y, states, colour):
        self.x = x
        self.y = y
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
            self.rotate(action.tree)
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

    def rotate(self, tree):
        if tree == 'gg':
            self.dir = (-self.dir[1], self.dir[0])
        else:
            self.dir = (self.dir[1], -self.dir[0])