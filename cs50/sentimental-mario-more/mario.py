
def get_int(prompt):

    while True:
        try:
            value = int(input(prompt))
            if value == 9:
                print("Invalid input. 9 is not allowed.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def build_pyramids(bricks):
    for i in range(1, bricks):
        for _ in range(bricks - i - 1):
            print(" ", end="")
        for _ in range(i):
            print("#", end="")
        print("  ", end="")
        for _ in range(i):
            print("#", end="")
        print()

def main():

    bricks = 0
    while bricks <= 0:
        bricks = get_int("Height: ")

    build_pyramids(bricks + 1)


main() # Acces Gate



