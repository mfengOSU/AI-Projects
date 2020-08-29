from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # If A is knight, A is a Knight and Knave OR
    # If A is knave, A is not a knight and a knave
    Or(And(AKnight,And(AKnight, AKnave)),And(AKnave,Not(And(AKnight,AKnave))))
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a knight or knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B is either a knight or knave but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # If A is knight, A and B are knaves OR 
    # If A is knave, A and B are not both knaves
    Or(And(AKnight, And(AKnave, BKnave)),And(AKnave,Not(And(AKnave, BKnave))))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either a knight or knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B is either a knight or knave but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # If A is knight, A and B are both knights OR
    # If A is knave, A is knave and B is knight
    Or(And(AKnight, And(AKnight, BKnight)),And(AKnave, And(AKnave, BKnight))),
    # If B is knight,  B is knight and A is knave OR
    # If B is knave, A and B or both knaves
    Or(And(BKnight, And(BKnight, AKnave)),And(BKnave,And(BKnave, AKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is either a knight or knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B is either a knight or knave but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # C is either a knight or knave but not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # If C is knight, A is knight OR 
    # If C is knave, A is not knight
    Or(And(CKnight, AKnight), And(CKnave, Not(AKnight))),
    # If B is knight, C is knave OR 
    # If B is knave, C is not knave
    Or(And(BKnight, CKnave), And(BKnave, Not(CKnave))),
    # If B is knight, A is knave OR 
    # If B is knave, A is not knave
    Or(And(BKnight, AKnave), And(BKnave, Not(AKnave))),
    # If A is knight, A is either knight or knave but don't know OR
    # If A is knave, A is not either knight or knave
    Or(And(AKnight, Or(AKnight, AKnave)), And(AKnave, Not(Or(AKnight, AKnave))))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
