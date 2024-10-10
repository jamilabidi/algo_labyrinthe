import random
from collections import deque

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = None
        self.start = (0, 0)
        self.goal = (height - 1, width - 1)

    def generate_maze(self):
        max_attempts = 100
        for attempt in range(max_attempts):
            self.grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
            self.grid[self.start[0]][self.start[1]] = 'S'
            self.grid[self.goal[0]][self.goal[1]] = 'G'
            self._generate_paths()
            
            if self._is_solvable():
                print(f"Labyrinthe solvable généré après {attempt + 1} tentatives.")
                return
        
        print(f"Échec de génération d'un labyrinthe solvable après {max_attempts} tentatives.")
        self._generate_fallback_maze()

    def _generate_paths(self):
        walls = []
        self._add_walls(self.start, walls)
        while walls:
            wall = random.choice(walls)
            walls.remove(wall)
            x, y = wall
            if self._can_be_path(x, y):
                self.grid[x][y] = '0'
                self._add_walls((x, y), walls)

    def _add_walls(self, cell, walls):
        x, y = cell
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < self.height and 0 <= ny < self.width and self.grid[nx][ny] == '#':
                walls.append((x + dx, y + dy))

    def _can_be_path(self, x, y):
        count = sum(1 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    if 0 <= x+dx < self.height and 0 <= y+dy < self.width and self.grid[x+dx][y+dy] == '0')
        return count == 1

    def _is_solvable(self):
        queue = deque([self.start])
        visited = set([self.start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.goal:
                return True
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width and (nx, ny) not in visited and self.grid[nx][ny] != '#':
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        return False

    def _generate_fallback_maze(self):
        self.grid = [['0' for _ in range(self.width)] for _ in range(self.height)]
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.goal[0]][self.goal[1]] = 'G'
        for _ in range(int(self.width * self.height * 0.3)):
            x, y = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
            if (x, y) != self.start and (x, y) != self.goal:
                self.grid[x][y] = '#'

    def display(self):
        for row in self.grid:
            print(' '.join(row))
        print()

class Maze:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

    def is_within_bounds(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def is_wall(self, x, y):
        return self.grid[x][y] == '#'

    def is_goal(self, x, y):
        return (x, y) == self.goal

    def display(self, player_position):
        print("\nLabyrinthe:")
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if (i, j) == player_position:
                    print("P", end=" ")
                elif (i, j) == self.goal:
                    print("G", end=" ")
                elif cell == '#':
                    print("#", end=" ")
                elif cell == 'x':
                    print("x", end=" ")
                elif (i, j) == self.start:
                    print("S", end=" ")
                else:
                    print(".", end=" ")
            print()
        print(f"Position actuelle : {player_position}\n")

class Player:
    def __init__(self, maze):
        self.maze = maze
        self.visited = set()
        self.moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.exploration_order = []
        self.order = 0
        self.parents = {}

    def bfs(self):
        queue = deque([self.maze.start])
        self.visited.add(self.maze.start)
        self.order += 1
        self.exploration_order.append((self.order, self.maze.start))
        self.parents[self.maze.start] = None

        while queue:
            x, y = queue.popleft()
            if self.maze.is_goal(x, y):
                print(f"Arrivée trouvée à {(x, y)}")
                self.display_exploration_order()
                self.total_length_exploration()
                self.compute_shortest_path((x, y))
                return True

            for dx, dy in self.moves:
                nx, ny = x + dx, y + dy
                if self.maze.is_within_bounds(nx, ny) and not self.maze.is_wall(nx, ny) and (nx, ny) not in self.visited:
                    queue.append((nx, ny))
                    self.visited.add((nx, ny))
                    self.maze.grid[nx][ny] = 'x'
                    self.maze.display((nx, ny))
                    self.order += 1
                    self.exploration_order.append((self.order, (nx, ny)))
                    self.parents[(nx, ny)] = (x, y)

        print("Pas de chemin vers la sortie.")
        self.display_exploration_order()
        self.total_length_exploration()
        return False

    def display_exploration_order(self):
        print("Chemin d'exploration:")
        print(", ".join(f"{order}({x},{y})" for order, (x, y) in self.exploration_order))

    def total_length_exploration(self):
        print(f"Nombre total de mouvements: {len(self.exploration_order)}")

    def find_exit(self):
        if not self.bfs():
            print("Pas de chemin vers la sortie.")

    def compute_shortest_path(self, goal):
        path = []
        current = goal
        while current:
            path.append(current)
            current = self.parents[current]
        path.reverse()
        print("Chemin le plus court:")
        print(" -> ".join(f"({x},{y})" for x, y in path) + " -> Arrivée")

# Utilisation
width, height = 40, 30

maze_generator = MazeGenerator(width, height)
maze_generator.generate_maze()
maze_generator.display()

maze = Maze(maze_generator.grid, maze_generator.start, maze_generator.goal)
player = Player(maze)
player.find_exit()