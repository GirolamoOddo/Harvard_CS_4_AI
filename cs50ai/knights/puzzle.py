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
    Or(AKnight, AKnave),                  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),            # A cannot be both a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)),    # If A is a knight, then A is both a knight and a knave (which is impossible)
    Implication(AKnave, Not(And(AKnight, AKnave))) # If A is a knave, then it's not true that A is both a knight and a knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),                  # A is either a knight or a knave
    Or(BKnight, BKnave),                  # B is either a knight or a knave
    Not(And(AKnight, AKnave)),            # A cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),            # B cannot be both a knight and a knave
    Implication(AKnight, And(AKnave, BKnave)),    # If A is a knight, then A and B are both knaves
    Implication(AKnave, Not(And(AKnave, BKnave))) # If A is a knave, then it is not true that A and B are both knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),                      # A is either a knight or a knave
    Or(BKnight, BKnave),                      # B is either a knight or a knave
    Not(And(AKnight, AKnave)),                # A cant be both a knight and a knave
    Not(And(BKnight, BKnave)),                # B cant be both a knight and a knave
    Implication(AKnight, Biconditional(AKnight, BKnight)),      # If A is a knight, then A and B are of the same kind
    Implication(AKnave, Not(Biconditional(AKnight, BKnight))),  # If A is a knave, then A and B are not of the same kind
    Implication(BKnight, Not(Biconditional(AKnight, BKnight))), # If B is a knight, then A and B are of different kinds
    Implication(BKnave, Biconditional(AKnight, BKnight))        # If B is a knave, then A and B are of the same kind
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),                      # A is either a knight or a knave
    Or(BKnight, BKnave),                      # B is either a knight or a knave
    Or(CKnight, CKnave),                      # C is either a knight or a knave
    Not(And(AKnight, AKnave)),                # A cant be both a knight and a knave
    Not(And(BKnight, BKnave)),                # B cant be both a knight and a knave
    Not(And(CKnight, CKnave)),                # C cant be both a knight and a knave

    # A says "I am either a knight or a knave"
    # This is always true, so we don't need to explicitly add this to the knoledge

    # B says "A said 'I am a knave'"
    Implication(BKnight, Biconditional(AKnight, AKnave)), #If B is a knight, then B's statement is true and A said 'I am a knave'
    Implication(BKnave, Not(Biconditional(AKnight, AKnave))),  # If B is a knave, then B's statement is false and A didn't say 'I am a knave'

    # B says "C is a knave"
    Implication(BKnight, CKnave),      # If B is a knight, then C is a knave
    Implication(BKnave, Not(CKnave)),  # If B is a knave, then C is not a knave

    # C says "A is a knight"
    Implication(CKnight, AKnight),   # If C is a knight, then A is a knight
    Implication(CKnave, Not(AKnight))  # If C is a knave, then A is not a knight
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
