import random
from collections import deque

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['#' for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.goal = self._random_position()

    def _random_position(self):
        return (random.randint(0, self.height - 1), random.randint(0, self.width - 1))

    def generate_maze(self):
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.goal[0]][self.goal[1]] = 'G'
        self._generate_paths()
        
        max_attempts = 100
        attempts = 0
        while not self._is_solvable() and attempts < max_attempts:
            self.grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
            self.grid[self.start[0]][self.start[1]] = 'S'
            self.goal = self._random_position()
            self.grid[self.goal[0]][self.goal[1]] = 'G'
            self._generate_paths()
            attempts += 1
        
        if attempts == max_attempts:
            print("Impossible de générer un labyrinthe solvable après 100 tentatives.")
            self._generate_simple_maze()

    def _generate_simple_maze(self):
        self.grid = [['0' for _ in range(self.width)] for _ in range(self.height)]
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.goal[0]][self.goal[1]] = 'G'
        # Ajouter quelques murs aléatoires
        for _ in range(int(self.width * self.height * 0.3)):  # 30% de murs
            x, y = self._random_position()
            if (x, y) != self.start and (x, y) != self.goal:
                self.grid[x][y] = '#'

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
        """
        Initialise le labyrinthe avec la grille, le point de départ et le point d'arrivée.
        """
        self.grid = grid
        self.start = start
        self.goal = goal

    def is_within_bounds(self, x, y):
        """
        Vérifie si une position (x, y) est à l'intérieur des limites du labyrinthe.
        """
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def is_wall(self, x, y):
        """
        Vérifie si une position (x, y) est un mur (valeur = 1).
        """
        return self.grid[x][y] == 1

    def is_goal(self, x, y):
        """
        Vérifie si une position (x, y) est l'arrivée (G).
        """
        return (x, y) == self.goal

    def display(self, player_position):
        """
        Affiche le labyrinthe à chaque étape avec la position du joueur.
        """
        print("\nLabyrinthe:")
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if (i, j) == player_position:
                    print("P", end=" ")  # P pour la position actuelle
                elif (i, j) == self.goal:
                    print("G", end=" ")  # G pour l'arrivée
                elif self.grid[i][j] == 1:
                    print("#", end=" ")  # # pour les murs
                elif self.grid[i][j] == 'x':
                    print("x", end=" ")  # x pour les chemins visités
                elif (i, j) == self.start:
                    print("S", end=" ")  # S pour le point de départ
                else:
                    print(".", end=" ")  # . pour les chemins non visités
            print()
        print(f"Position actuelle : {player_position}\n")


class Player:
    def __init__(self, maze):
        """
        Initialise le joueur avec le labyrinthe et garde trace des positions visitées.
        """
        self.maze = maze
        self.visited = set()
        self.path = []
        self.moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Droite, bas, gauche, haut
        self.exploration_order = []
        self.order = 0

    def dfs(self, position):
        """
        Algorithme DFS récursif pour explorer le labyrinthe à partir d'une position donnée.
        """
        x, y = position

        # Si l'arrivée est atteinte, on arrête
        if self.maze.is_goal(x, y):
            self.order += 1
            self.exploration_order.append((self.order, position))
            print(f"Arrivée trouvée à {position}")
            self.display_exploration_order()
            self.total_length_exploration()
            return True

        # Marquer la position comme visitée
        self.visited.add(position)
        self.path.append(position)
        self.maze.grid[x][y] = 'x'
        self.order += 1
        self.exploration_order.append((self.order, position))
        self.maze.display(position)

        # Essayer chaque mouvement possible
        for move in self.moves:
            new_x, new_y = x + move[0], y + move[1]

            # Vérifier si la nouvelle position est valide (dans le labyrinthe, pas un mur, et pas déjà visitée)
            if self.maze.is_within_bounds(new_x, new_y) and not self.maze.is_wall(new_x, new_y) and (new_x, new_y) not in self.visited:
                # Appel récursif pour continuer l'exploration
                if self.dfs((new_x, new_y)):
                    return True

        # Backtrack: remove the position from path if no valid path is found
        self.path.pop()
        self.order += 1
        self.exploration_order.append((self.order, position))
        return False

    def display_exploration_order(self):
        """
        Affiche le chemin d'exploration avec le numéro d'ordre et les coordonnées.
        """
        print("Chemin d'exploration:")
        for order, position in self.exploration_order:
            print(f"{order}({position[0]},{position[1]})", end=" , ")
        print()

    def total_length_exploration(self):
        """
        Affiche le nombre total de mouvements effectués pour arriver à une des conditions de fin du jeu.
        """
        total_moves = len(self.exploration_order)
        print(f"Nombre total de mouvements: {total_moves}")

    def find_exit(self):
        """
        Démarre la recherche DFS à partir du point de départ.
        """
        if not self.dfs(self.maze.start):
            print("Pas de chemin vers la sortie.")


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


# Utilisation
width, height = 40, 30

maze_generator = MazeGenerator(width, height)
maze_generator.generate_maze()
maze_generator.display()

maze = Maze(maze_generator.grid, maze_generator.start, maze_generator.goal)
player = Player(maze)
player.find_exit()
