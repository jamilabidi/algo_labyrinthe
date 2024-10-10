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
                elif self.grid[i][j] == 1:
                    print("#", end=" ")  # # pour les murs
                elif (i, j) == self.start:
                    print("S", end=" ")  # S pour le point de départ
                elif (i, j) == self.goal:
                    print("G", end=" ")  # G pour l'arrivée
                elif (i, j) in self.visited:
                    print(".", end=" ")
                else:
                    print("?", end=" ")  # . pour les chemins non visités
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
        self.moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Est, Sud, Ouest, Nord

    def dfs(self, position):
        """
        Algorithme DFS pour explorer le labyrinthe à partir d'une position donnée.
        """
        x, y = position

        # Si l'arrivée est atteinte, on arrête
        if self.maze.is_goal(x, y):
            print(f"Arrivée trouvée à {position}")
            self.path.append(position)
            return True

        # Marquer la position comme visitée
        self.visited.add(position)
        self.maze.display(position)

        # Essayer chaque mouvement possible
        for move in self.moves:
            new_x, new_y = x + move[0], y + move[1]

            # Vérifier si la nouvelle position est valide (dans le labyrinthe, pas un mur, et pas déjà visitée)
            if self.maze.is_within_bounds(new_x, new_y) and not self.maze.is_wall(new_x, new_y) and (new_x, new_y) not in self.visited:
                # Appel récursif pour continuer l'exploration
                if self.dfs((new_x, new_y)):
                    self.path.append(position)
                    return True

        return False

    def find_exit(self):
        """
        Démarre la recherche DFS à partir du point de départ.
        """
        if not self.dfs(self.maze.start):
            print("Pas de chemin vers la sortie.")
        else:
            print(f"Chemin vers la sortie : {self.path[::-1]}")
            print(f"Nombre d'étapes : {len(self.path)}")


# Initialisation du labyrinthe (0 = chemin, 1 = mur, 'S' = départ, 'G' = arrivée)
labyrinthe_grid = [
    ['S', 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0],
    [1, 0, 1, 'G', 1, 0],
    [1, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0]
]

# Coordonnées de départ (0, 0) et d'arrivée (5, 5)
start_position = (0, 0)
goal_position = (2, 3)

# Création d'une instance de Maze et Player
maze = Maze(labyrinthe_grid, start_position, goal_position)
player = Player(maze)

# Lancement de la recherche du chemin
player.find_exit()
