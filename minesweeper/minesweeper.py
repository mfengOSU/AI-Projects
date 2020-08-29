import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        # If count equals the number of cells, then all cells are mines
        if self.count == len(self.cells):
            mines.update(self.cells)
        return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        mines = set()
        # If count is 0, then no cells are mines
        if self.count == 0:
            mines.update(self.cells)
        return mines

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is a mine in sentence, then remove it and decrease count by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell is safe in sentence, remove it
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark cell as safe 
        self.mark_safe(cell=cell)
        # Add cell to moves made
        self.moves_made.add(cell)
        # Get the distances to the cell's neighbors
        coordinates = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        # Check if cell's neighbors are valid coordinates and undetermined. 
        # If so, add the neighbor cell to a new sentence
        neighbor_cells = set()
        for coordinate in coordinates:
            new_cell = tuple(map(lambda x, y: x + y, coordinate, cell))
            if(
                new_cell[0] >= 0 and new_cell[1] >= 0 
                and new_cell[0] < self.width and new_cell[1] < self.height
                and (new_cell not in self.mines and new_cell not in self.safes and new_cell not in self.moves_made)          
                ):
                neighbor_cells.add(new_cell)
            # If neighbor cell is a mine, decrease count by 1
            if new_cell in self.mines:
                count -= 1
        
        # Add the new sentence about the neighbor cells if non-empty
        if len(neighbor_cells) > 0:
            new_sentence = Sentence(cells=neighbor_cells, count=count)
            self.knowledge.append(new_sentence)

        # Check if sentences in KB are subsets of one another
        # If so add the new sentences to KB
        new_sentences = []
        for sentence in self.knowledge:
            for sentence2 in self.knowledge:
                if not sentence.__eq__(sentence2) and len(sentence.cells) > 0:
                    if sentence.cells.issubset(sentence2.cells):
                        new_cells = sentence2.cells.difference(sentence.cells)
                        new_count = sentence2.count - sentence.count
                        new_sentences.append(Sentence(cells=new_cells, count=new_count))

        for sentence in new_sentences:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)

        # For each sentence in KB, update any additional cells as safe or mines
        for sentence in self.knowledge:
            safe = sentence.known_safes()
            mine = sentence.known_mines()
            for safe_square in safe:
                if safe_square not in self.safes:
                    self.mark_safe(cell=safe_square)
            for mine_square in mine:
                if mine_square not in self.mines:
                    self.mark_mine(cell=mine_square)
                        
        



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Generate a safe move that has not been played.
        # Otherwise no safe moves can be played
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Return none if no moves left to make
        if (self.height * self.width) == len(self.moves_made) + len(self.mines):
            return None
        # Generate random x, y coordinate within the width and height of board
        random.seed()
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        # Continously generate random move until move has not been chosen and is not mine
        while True:
            if (x, y) not in self.moves_made and (x, y) not in self.mines:
                return (x, y)
            x = random.randrange(self.width)
            y = random.randrange(self.height)