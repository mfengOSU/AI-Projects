import sys
import time
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Set of words that are inconsistent with variable's unary constraint
        removed = set()

        # Loop through each dict item
        for var, words in self.domains.items():
            # Loop through each set of words corresponding to 
            # the particular variable
            for word in words:
                # If length of word is not the same as variable length, remove word
                if len(word) != var.length:
                    removed.add(word)
            self.domains[var] = self.domains[var] - removed
            removed.clear()

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        # Get the overlap, if any, between variables x and y
        overlap = self.crossword.overlaps[x, y]
        # Set of words in self.domains[x] that have no possible corresponding
        # value for y in self.domains[y]
        removed = set()

        # Only revise domain of x if there is an overlap between x and y
        if overlap != None:
            # Loop through each word in x's domain
            for word in self.domains[x]:
                has_value = False
                # Loop through each word in y's domain
                for word2 in self.domains[y]:
                    # Check if the overlapped character is the same for 
                    # 2 words in domains of x and y
                    if word[overlap[0]] == word2[overlap[1]]:
                        has_value = True
                        break
                # If word has no corresponding value, remove the word
                # and set revised to True
                if not has_value:
                    removed.add(word)
                    revised = True
            self.domains[x] = self.domains[x] - removed
        return revised
                

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # List of arcs in problem
        queue = list()
        # If no arcs provided, set queue to be list of all initial
        # arcs in problem
        if arcs == None:
            for var in self.domains.keys():
                neighbors = self.crossword.neighbors(var=var)
                for var2 in neighbors:
                    queue.append((var, var2))
        # Otherwise, use the arcs provided
        else:
            queue = arcs.copy()
        
        # Revise each arc one at a time, to ensure
        # each variable is arc consistent
        while len(queue) > 0:
            (x, y) = queue.pop(0)
            # Check if domain of x was revised
            if self.revise(x=x, y=y):
                # Check if domain of x is empty, which means no solution
                if len(self.domains[x]) == 0:
                    return False
                # Add additional arcs to queue if domain of x was revised
                # to ensure other arcs stay consistent
                for z in self.crossword.neighbors(var=x) - {y}:
                    queue.append((z, x))
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if each variable is assigned. If not, return False
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Set of words used to assign each variable in assignment
        unique_words = set()
        # Loop through each item in assignment
        for var, word in assignment.items():
            # Check if the words in assignment are distinct
            if word in unique_words:
                return False
            # Check if words in assignment are correct length
            if len(word) != var.length:
                return False
            unique_words.add(word)
            # Check if words conflict with each other
            neighbors = self.crossword.neighbors(var=var)
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if neighbor in assignment:
                    if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False          
        return True

        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Dictonary mapping the words in domain of var to the number of 
        # values they rule out for neighboring variables
        constraint = dict()
        # Get the neighbor variables of var that aren't in assignment
        neighbors = self.crossword.neighbors(var=var) - set(assignment.keys())

        # Loop through each word in var's domain
        for word in self.domains[var]:
            num_values = 0
            # Loop through each neighbor variable of var not in assignment
            for neighbor in neighbors:
                # Get overlap between var and a unassigned neighbor variable
                overlap = self.crossword.overlaps[var, neighbor]
                # Loop through each word in domain of the neighbor variable
                for word2 in self.domains[neighbor]:
                    # If the two words' overlapped characters conflict,
                    # increment num_values
                    if word[overlap[0]] != word2[overlap[1]]:
                        num_values += 1
            # Update dictionary
            constraint[word] = num_values

        # Sort keys in constraint dictionary by least to greatest by number of values ruled out
        values_sorted = sorted(constraint.keys(), key=constraint.get)

        return values_sorted

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # list of unassigned variables in order by number of values in its domain
        unassigned = list()
        # List of unassigned variables sorted by their degree
        degree_order = list()

        # Sort variables by number of values in the variable's domain
        domain_sorted = sorted(self.domains.keys(), key=lambda k:len(self.domains[k]))

        # Keep track of unassigned variables in the correct order
        for var in domain_sorted:
            if var not in assignment:
                unassigned.append(var)
        # Return the first unassigned variable if only one unassigned variable
        if len(unassigned) < 2:
            return unassigned[0]
        # Get min number of remaining values in a variable's domain
        min_value = len(self.domains[unassigned[0]])
        # Loop through unassigned variables
        # and add all variables with the min_value to a new list
        for var in unassigned:
            if len(self.domains[var]) == min_value:
                degree_order.append(var)

        # If only one variable with the min_value, return it
        if len(degree_order) < 2:
            return degree_order[0]

        # Set an initial highest degree
        highest_degree = len(self.crossword.neighbors(var=degree_order[0]))
        # Set an initial highest degree variable
        highest_degree_var = degree_order[0]

        # Loop through each unassigned variable with same min_value
        for var in degree_order:
            # Update highest_degree and highest_degree_var if there is a variable
            # with higher degree
            if len(self.crossword.neighbors(var=var)) > highest_degree:
                highest_degree = len(self.crossword.neighbors(var=var))
                highest_degree_var = var

        return highest_degree_var

    def inference(self, var):
        """
        Update `self.domains` by removing values that
        don't maintain arc consistency between variables
        """
        arcs = list()
        neighbors = self.crossword.neighbors(var=var)
        for neighbor in neighbors:
            arcs.append((neighbor, var))

        return self.ac3(arcs=arcs)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment=assignment):
            return assignment
        # Select unassigned variable
        unassigned = self.select_unassigned_variable(assignment=assignment)
        # Loop through each word in the unassigned variable's domain
        for value in self.order_domain_values(var=unassigned, assignment=assignment):
            # Clone assignment
            new_assignment = assignment.copy()
            # Assign value to variable
            new_assignment[unassigned] = value         
            self.print(assignment=new_assignment) 
            self.save(assignment=new_assignment, filename="output_before.png")
            print()
            time.sleep(0.3)
            # Check if assignment still consistent
            if self.consistent(assignment=new_assignment):
                # Update domain of the selected variable to just that value
                self.domains[unassigned] = {value}
                # Copy self.domains
                domains_copy = self.domains.copy() 
                # Make inferences based on assignment
                inferences = self.inference(var=unassigned)
                # Check if inference is not failure
                if inferences != False:
                    # If so, recursively call backtrack on new assignment
                    result = self.backtrack(assignment=new_assignment)
                    # If not a failure, return the assignment
                    if result != None:
                        return result
                # Restore original domain if inferences was failure
                else:
                    self.domains.update(domains_copy)
            
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
