# Kuhn Poker — Counterfactual Regret Minimization (CFR)

A minimal Python implementation of the **Counterfactual Regret Minimization (CFR)** algorithm applied to **Kuhn Poker** — one of the simplest non-trivial poker variants used to study game theory and Nash equilibria.

---

## What is Kuhn Poker?

Kuhn Poker is a two-player card game using only three cards: **King (K), Queen (Q), and Jack (J)**. Each player is dealt one card, and one round of betting takes place.

**Rules:**

- Each player antes 1 chip
- Player 1 acts first: **Bet** or **Check**
- If Player 1 **Bets** → Player 2 can **Call** or **Fold**
- If Player 1 **Checks** → Player 2 can **Bet** or **Check**
- If Player 2 **Bets** after a Check → Player 1 can **Call** or **Fold**
- Highest card wins at showdown (K > Q > J)

**Terminal histories:** `UU` (check-check), `BC` (bet-call), `BF` (bet-fold)

---

## What is CFR?

**Counterfactual Regret Minimization** is a self-play algorithm that iteratively reduces regret for each action at every decision point (infoset). Over many iterations, the average strategy converges to a **Nash Equilibrium**.

At each infoset, the algorithm:

1. Computes the counterfactual value of each action
2. Updates regret sums based on missed value
3. Derives a new mixed strategy proportional to positive regrets
4. Accumulates the average strategy over all iterations

---

## Nash Equilibrium Results

After ~165,000 training iterations, the algorithm converges to the theoretical Nash Equilibrium for Kuhn Poker.

### Bet Probabilities (Player 1 opening)

![Bet Probabilities](/Library/fig1.png)

| Card | Converged Bet Probability | Interpretation                             |
| ---- | ------------------------- | ------------------------------------------ |
| K    | ~1.0                      | Always bet with the best hand              |
| Q    | ~0.0                      | Never bluff with the middle card           |
| J    | ~0.33                     | Bluff ~1/3 of the time with the worst hand |

### Check Probabilities (Player 1 opening)

![Check Probabilities](/Library/fig2.png)

| Card | Converged Check Probability | Interpretation                             |
| ---- | --------------------------- | ------------------------------------------ |
| K    | ~0.0                        | Never check with the best hand             |
| Q    | ~1.0                        | Always check with the middle card          |
| J    | ~0.67                       | Check ~2/3 of the time with the worst hand |

These results match the **known analytical Nash Equilibrium** for Kuhn Poker, validating the implementation.

---

## Project Structure

```
.
├── main.py       # Main implementation
└── README.md
```

### Key Components

- **`Node`** — Represents an information set. Stores strategy, regret sums, and strategy sums.
- **`cfr()`** — Recursive CFR traversal. Returns expected utility and updates regrets.
- **`train()`** — Runs 165,000 iterations, samples random card deals, and plots convergence.
- **`terminal()`** — Detects terminal game states from history string.
- **`payoff()`** — Computes the reward at terminal nodes.

---

## Running the Code

**Requirements:**

```bash
pip install numpy matplotlib
```

**Run:**

```bash
python kuhn_cfr.py
```

This will train the CFR agent and display the convergence plots for all card/action combinations.

---

## References

- Kuhn, H. W. (1950). _Simplified Two-Person Poker_
- Zinkevich et al. (2007). _Regret Minimization in Games with Incomplete Information_
- Neller & Lanctot (2013). _An Introduction to Counterfactual Regret Minimization_ — a great beginner resource
