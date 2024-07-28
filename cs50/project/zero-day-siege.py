

import random

#PARAMS-------------------------------------------------------------------------

# ATTACKER SETTING

DEPTH = 5 # MinMax search depth, have to be odd (=<7 suggested)

# GAME SETTINGS (Explore differents game dynamics)

MAX_ATT_SCORE = 4 # =< 4
MAX_DEF_SCORE = 4 # =< 4

ATT_COOLDOWN  = 4 # 4
DEF_COOLDOWN  = 6 # 6

# vul. value to get +1 on score
MIN_VULNERABILITY = 0 # 0
MAX_VULNERABILITY = 5 # 5

#-------------------------------------------------------------------------------

def evaluate_state(state, attacker_score, defender_score):
    attacker_advantage = attacker_score - defender_score
    attacker_winning = +10 if attacker_score == MAX_ATT_SCORE else 0
    defender_winning = -10 if defender_score == MAX_DEF_SCORE else 0
    return round(attacker_advantage, 4) + attacker_winning + defender_winning

def min_max(state, cooldown, attacker_score, defender_score, depth, player, alpha, beta):
    if depth == 0 or attacker_score >= MAX_ATT_SCORE or defender_score >= MAX_DEF_SCORE:
      return None, evaluate_state(state, attacker_score, defender_score), attacker_score, defender_score

    cooldown_sim = cooldown.copy()
    if depth != DEPTH: #  avoiding the first minmax call
       for i in range(len(cooldown_sim)):
           cooldown_sim[i] = max(0, cooldown_sim[i] - 1)

    best_move = None
    if player == 'attacker':
        best_score = float('-inf')
        for i in range(len(state)):
            if state[i] > MIN_VULNERABILITY and state[i] < MAX_VULNERABILITY and cooldown_sim[i] == 0:
                state[i] += 1
                cooldown_sim[i] = ATT_COOLDOWN
                attacker_score = state.count(MAX_VULNERABILITY)

                _, score, _, _ = min_max(state, cooldown_sim, attacker_score, defender_score, depth - 1, 'defender', alpha, beta)

                state[i] -= 1
                cooldown_sim[i] = 0
                attacker_score = state.count(MAX_VULNERABILITY)
                if score > best_score:
                    best_score = score
                    best_move = i
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_move, best_score, attacker_score, defender_score
    else:
        best_score = float('inf')
        for i in range(len(state)):
            if state[i] > MIN_VULNERABILITY and state[i] < MAX_VULNERABILITY and cooldown_sim[i] == 0:
                state[i] -= 1
                cooldown_sim[i] = DEF_COOLDOWN
                defender_score = state.count(MIN_VULNERABILITY)

                _, score, _, _ = min_max(state, cooldown_sim, attacker_score, defender_score, depth - 1, 'attacker', alpha, beta)

                state[i] += 1
                cooldown_sim[i] = 0
                defender_score = state.count(MIN_VULNERABILITY)
                if score < best_score:
                    best_score = score
                    best_move = i
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_move, best_score, attacker_score, defender_score

def attacker_move(state, cooldown, attacker_score, defender_score, depth=DEPTH):
    alpha = float('-inf')
    beta  = float(' inf')
    best_move, best_score, attacker_score, defender_score = min_max(state, cooldown, attacker_score, defender_score, depth, 'attacker', alpha, beta)

    if best_move is not None:
        print(f"MinMax best score for depth {depth}: {best_score}")
        print(f"Attacker winning pattern found") if best_score >= float(' 4') else None
        print(f"Defender winning pattern found") if best_score <= float('-4') else None
        print(f"No valid moves situation for defender found") if best_score == float('inf') else None
        return best_move, state[best_move], attacker_score, defender_score
    else:
        print(f"MinMax best score for depth {depth}: {best_score}")
        print(f"No valid moves situation for attacker found")
        # Choose a suboptimal move by selecting the first valid move
        for i in range(len(state)):
            if state[i] > MIN_VULNERABILITY and state[i] < MAX_VULNERABILITY and cooldown[i] == 0:
               return i, state[i], attacker_score, defender_score

        # If no valid move is available, return None for move and unchanged state
        return None, None, attacker_score, defender_score

def defender_move(state, cooldown, attacker_score, defender_score):
    valid_moves = [i for i in range(len(state)) if state[i] > MIN_VULNERABILITY and state[i] < MAX_VULNERABILITY and cooldown[i] == 0]
    if not valid_moves:
        return None
    while True:
        move = int(input("Enter the vulnerability you want to patch (0-9): "))
        if move in valid_moves:
            return move, state[move], attacker_score, defender_score + state.count(MIN_VULNERABILITY)
        else:
            print(f"Invalid move! Please choose a vulnerability with a risk value between {MIN_VULNERABILITY+1} and {MAX_VULNERABILITY-1} and cooldown equal to 0.")

def play_round(state, cooldown, player_turn):
    print('-------------------------------------------------------------')
    attacker_score = state.count(MAX_VULNERABILITY)  # Update attacker's score
    defender_score = state.count(MIN_VULNERABILITY)  # Update defender's score
    print("Attacker's Score:", attacker_score)
    print("Defender's Score:", defender_score)
    print("Vulnerability   :", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print("Current state   :", state)
    print("Current cooldown:", cooldown)

    if attacker_score >= MAX_ATT_SCORE:
        print("Attacker wins!")
        return True
    elif defender_score >= MAX_DEF_SCORE:
        print("Defender wins!")
        return True

    if player_turn:
        print("Your turn...")
        move = defender_move(state, cooldown, attacker_score, defender_score)
        if move is None:
            print("No valid move for defender. Attacker wins!")
            return True
        print("Defender patches vulnerability:", move[0])
        state[move[0]] -= 1
        cooldown[move[0]] = DEF_COOLDOWN

    else:
        print("Attacker's turn...")
        move = attacker_move(state, cooldown, attacker_score, defender_score)
        # Check if move is not None before accessing its elements
        if move[0] is None:
            print("No valid move for attacker. Defender wins!")
            return True
        elif move[0] is not None:
            print("Attacker exploits vulnerability:", move[0])
            state[move[0]] += 1
            cooldown[move[0]] = ATT_COOLDOWN

    for i in range(len(cooldown)):
         cooldown[i] = max(0, cooldown[i] - 1)

    return False

def generate_random_initial_state():
    return [random.randint(2, 3) for _ in range(10)] # debug fixed start [0,5,0,4,0,1,4,5,3,3]

#-------------------------------------------------------------------------------

def main():

    print()
    print(r'''
__________                            ________                    _________.__
\____    /___________  ____           \______ \ _____  ___.__.   /   _____/|__| ____   ____   ____
  /     // __ \_  __ \/  _ \   ______  |    |  \\__  \<   |  |   \_____  \ |  |/ __ \ / ___\_/ __ \
 /     /\  ___/|  | \(  <_> ) /_____/  |    `   \/ __ \\___  |   /        \|  \  ___// /_/  >  ___/
/_______ \___  >__|   \____/          /_______  (____  / ____|  /_______  /|__|\___  >___  / \___  >
        \/   \/                               \/     \/\/               \/         \/_____/      \/
    ''')
    print()
    print("Welcome to Zero-Day Siege!")
    print("Rules:")
    print("- The game is played between a defender and an attacker.")
    print("- The defender's goal is to patch vulnerabilities.")
    print("- The attacker's goal is to exploit vulnerabilities.")
    print(f"- Each vulnerability has a risk rank from {MIN_VULNERABILITY} to {MAX_VULNERABILITY}.")
    print("- The defender patches vulnerabilities by reducing their risk rank by 1.")
    print("- The attacker exploits vulnerabilities by increasing their risk rank by 1.")
    print(f"- After being patched, a vulnerability cannot be patched/exploited again for {DEF_COOLDOWN-1} turns.")
    print(f"- After being exploited, a vulnerability cannot be patched/exploited again for {ATT_COOLDOWN-1} turns.")
    print(f"- The game ends when one player reaches a score of {MAX_ATT_SCORE}.") if MAX_ATT_SCORE == MAX_DEF_SCORE else print(f"- The game ends when attacker reach a score of: {MAX_ATT_SCORE} or defender reach a score of: {MAX_DEF_SCORE}.")

    print()

    initial_state = generate_random_initial_state()
    cooldown = [0] * len(initial_state)

    player_turn = True

    print('-------------------------------------------------------------')
    print('> MinMax Algorithm Play as Attacker!')
    print('Note: MinMax best score is the Euristic used for the search')
    print('      MinMax score is computed as Attacker_scr - Defender_scr')
    print('      if best_score >  4, means that an attacker winning line was found')
    print('      if best_score < -4, means that a  defender winning line was found')
    print()
    print('> You Play as Defender!')
    print('-------------------------------------------------------------')

    round = 0
    while True:
        print()
        print('Round:', int(round))
        round += 0.5
        if play_round(initial_state, cooldown, player_turn):
            break

        if all(cd == 1 for cd in cooldown):
            cooldown = [0] * len(initial_state)
        player_turn = not player_turn


if __name__ == "__main__":
    main()
