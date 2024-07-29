## ”α-β MiniMax Adversarial Intelligence for Simulating Cyber-Attacks”

#### ZERO-DAY SIEGE a Python Competitive Game
##### Girolamo Oddo

---
### __0. Overview:__

This project implements a zero-sum game that rapresent an ongoing cyber attack where user fight against an AI.

The game, in particular, involves two players: an attacker and a defender.
Each player takes turns to either exploit or patch vulnerabilities.

The vulnerabilities have risk ranks ranging from 0 to 5.
After being patched or exploited, a vulnerability enters in a cooldown period during which it cannot be targeted again.
The game ends when one player accumulates a score of 4, indicating a significant success in either exploitation or patching.
The score counter increse at each 0 or 5 reached respectivly by players.

---

### __1. Components of the Code:__
#### Game Logic Functions:
__play_round(state, cooldown, player_turn):__
>Manages the flow of a single round in the game.
attacker_move(state, cooldown, attacker_score, defender_score): Determines the attacker's move using the Minimax algorithm.
defender_move(state, cooldown, attacker_score, defender_score): Allows the defender to choose a vulnerability to patch.
generate_random_initial_state(): Initializes the game state with random vulnerability ranks.

#### Minimax Algorithm:
__min_max()__
>This function implements the Minimax algorithm with alpha-beta pruning to determine the best move for the attacker.
It evaluates possible future states of the game by recursively exploring the game tree up to a certain depth.
The algorithm alternates between maximizing the attacker's advantage and minimizing the defender's advantage, assuming both players play optimally.
The evaluate_state() function provides a heuristic evaluation of a game state based on the attacker's advantage.

#### Main Functionality:
__main()__
>This function initializes the game, provides instructions, and orchestrates the gameplay between the attacker and defender.
It prints the game state, prompts players for their moves, and updates the game accordingly until one player wins or the game ends in a draw.

---

### __2. AI Logic, Introduction to Minimax Algorithm and Adversarial Search:__

### Adversarial Search:
__Problem Space:__
Adversarial search deals with problems where multiple competing agents make decisions in an adversarial environment.
These problems are typically modeled as game trees, where each agent's actions affect the outcome of the game.

__Perfect Information Games:__
Adversarial search is commonly applied to games with perfect information, where all players have complete knowledge of the game state.
This includes classic board games like chess and Go.

__Strategic Decision Making:__
The goal of adversarial search is to develop strategies that lead to favorable outcomes, even in the face of opposition from other agents.
It involves exploring the space of possible actions and anticipating the moves of opponents to make informed decisions.

__Algorithmic Approaches:__
Various algorithms are used in adversarial search, including Minimax, Monte Carlo Tree Search (MCTS), and reinforcement learning techniques like Deep Q-Networks (DQN).
Each algorithm has its strengths and weaknesses, and the choice depends on factors such as the complexity of the game, the availability of computational resources, and the desired level of performance.

#### Minimax Algorithm:

__Decision Theory Foundation:__
The Minimax algorithm originates from decision theory, aiming to minimize the maximum possible loss (hence "minimax") in a worst-case scenario.
In game theory, it's particularly relevant for zero-sum games where the gain of one player directly corresponds to the loss of the other.

__Recursive Search:__
Minimax employs a recursive search through the game tree, where each level represents a player's turn and each node represents a possible game state.
At the leaf nodes, the game state is evaluated using a heuristic function, providing an estimate of the desirability of that state for the current player.

__Maximization and Minimization:__
The algorithm alternates between two types of nodes in the tree: maximizing nodes (for the player seeking to maximize their advantage) and minimizing nodes (for the opponent seeking to minimize that advantage).
At maximizing nodes, the algorithm selects the child node with the highest heuristic value, representing the best move for the current player.
At minimizing nodes, the algorithm selects the child node with the lowest heuristic value, representing the best countermove for the opponent.

__Alpha-Beta Pruning:__
Alpha-beta pruning is an optimization technique for the minimax algorithm. It reduces the number of nodes evaluated by the minimax algorithm by pruning branches that cannot influence the final decision, thus improving efficiency. The algorithm maintains two values, alpha (the best already explored option along the path to the maximizer) and beta (the best already explored option along the path to the minimizer), and stops evaluating a move when it finds that it is worse than a previously examined move.

__Time Complexity:__
The basic minimax algorithm has a time complexity of \(O(b^d)\), where \(b\) is the branching factor (the average number of child nodes per node) and \(d\) is the depth of the tree. This exponential growth makes the algorithm computationally expensive for deeper trees. Alpha-beta pruning can significantly reduce the number of nodes that need to be evaluated, potentially bringing the time complexity down to \(O(b^(d/2))\) in the best case. This reduction is achieved by eliminating branches that do not affect the final decision, thus making the algorithm more efficient.

---

### __3. Game Design Choices:__

### Vulnerabilities:
Range and Values: Vulnerabilities are assigned risk ranks ranging from 0 (minimum) to 5 (maximum). A vulnerability with a rank of 0 is fully patched, while a rank of 5 indicates a fully exploited vulnerability.
Attacker Score: The attacker's score increases by +1 for each vulnerability they exploit to the maximum value (5).
Defender Score: The defender's score increases by +1 for each vulnerability they patch to the minimum value (0).
The choice of the number of vulnerabilities and their value has been adjusted so as to make the game experience ragineable as duration and ensure that one player always wins over the other

### Cooldowns:
Attacker Cooldown: After the attacker exploits a vulnerability, it cannot be modified for 4 turns. This cooldown period forces the attacker to strategically choose which vulnerabilities to exploit and prevents them from repeatedly targeting the same vulnerability.
Defender Cooldown: After the defender patches a vulnerability, it cannot be modified for 6 turns. This longer cooldown period makes it challenging for the defender to keep up with the attacker and adds tension to the game by requiring careful selection of vulnerabilities to patch.

---

### __4. Usage:__

### Running the Game
1. **Open a terminal or command prompt**: Navigate to the directory where you saved `zero-day-siege.py`.

2. **Execute the script**: Run the game by typing the following command:
   ```sh
   python3 zero_day_siege.py
### Playing the Game
__Game Start:__ The game starts with a welcome message and rules explanation. You'll be informed that you play as the defender, and the MinMax algorithm plays as the attacker.

__Game Display:__ Each round displays the current scores, vulnerability states, and cooldowns:

Attacker's Score: Number of fully exploited vulnerabilities (rank 5).
Defender's Score: Number of fully patched vulnerabilities (rank 0).
Vulnerability: List of vulnerability indices.
Current state: List of current vulnerability risk ranks.
Current cooldown: List of cooldowns for each vulnerability.
Your Turn: When it's your turn as the defender:

You are prompted to choose a vulnerability to patch by entering its index (0-9).
You can only patch vulnerabilities with a risk rank between 1 and 4 and with a cooldown of 0.
Attacker's Turn: The MinMax algorithm makes its move to exploit vulnerabilities, following its strategic calculations.

End of Game: The game continues until either the attacker or defender reaches their maximum score (4), and the winner is declared.

Example Session:
```py
Welcome to Zero-Day Siege!
Rules:
- The game is played between a defender and an attacker.
- The defender's goal is to patch vulnerabilities.
- The attacker's goal is to exploit vulnerabilities.
- Each vulnerability has a risk rank from 0 to 5.
- The defender patches vulnerabilities by reducing their risk rank by 1.
- The attacker exploits vulnerabilities by increasing their risk rank by 1.
- After being patched, a vulnerability cannot be patched/exploited again for 5 turns.
- After being exploited, a vulnerability cannot be patched/exploited again for 3 turns.
- The game ends when one player reaches a score of 4.

-------------------------------------------------------------
> MinMax Algorithm Play as Attacker!
Note: MinMax best score is the Euristic used for the search
      MinMax score is computed as Attacker_scr - Defender_scr
      if best_score >  4, means that an attacker winning line was found
      if best_score < -4, means that a  defender winning line was found

> You Play as Defender!
-------------------------------------------------------------

Round: 0
-------------------------------------------------------------
Attacker's Score: 0
Defender's Score: 0
Vulnerability   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Current state   : [2, 3, 3, 2, 2, 2, 3, 3, 2, 3]
Current cooldown: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Your turn...
Enter the vulnerability you want to patch (0-9): 4
Defender patches vulnerability: 4 #<-- Your Input!
```
---

### __4. EXTRA Unaxpected Implementation Problems:__

The main issues that arose during the game implementation were:
- Properly handling cooldowns and their onset and disappearance in the search algorithm.
- Managing end-game scenarios where no moves were available, causing the AI to oscillate between reporting a winning and losing condition.
- Management of situations where no moves emerge as better than others. This condition must include a method to choose between moves of equal value to continue the game, with the current method being to select the first move among the equally valued choices.


---
