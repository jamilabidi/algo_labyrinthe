
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


# Initialisation du labyrinthe (0 = chemin, 1 = mur, 'S' = départ, 'G' = arrivée)
labyrinthe_grid = [
    ['S', 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0],
    [1, 0, 1, 'G', 1, 0],
    [1, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0]
]

# Coordonnées de départ (0, 0) et d'arrivée (2, 3)
start_position = (0, 0)
goal_position = (2, 3)

# Création d'une instance de Maze et Player
maze = Maze(labyrinthe_grid, start_position, goal_position)
player = Player(maze)

# Lancement de la recherche du chemin
player.find_exit()