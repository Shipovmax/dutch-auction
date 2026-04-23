# Dutch Auction

A console-based Dutch auction simulation game written in Python.  
Bid on flower lots as the price drops in real time, competing against AI players.

---

## How It Works

In a Dutch auction the price starts high and decreases over time. The first player to accept the current price wins the lot. Wait too long and an AI opponent might snatch it first.

**Game loop:**
1. A random lot from 12 flower products is selected each round.
2. The current price starts at the opening price and drops by 1,000 ₽ each tick.
3. On every tick you choose to buy, wait, view the leaderboard, or skip.
4. If you wait, the AI players evaluate the price and may buy instead.
5. The price cannot fall below the cost basis.
6. The game runs for 10 rounds.

**Profit formula:** `purchase_price × 1.3` — each lot is resold at 130% of the purchase price.

---

## Features

- **6 AI competitors** — each with a balance, preferred flowers, and disliked flowers that influence their bidding probability
- **12 flower lots** — Roses, Orchids, Sakura, Peonies, and more, each with unique quantities, start prices, and cost bases
- **Probabilistic AI** — buy chance is calculated from affordability, price level, and product preferences
- **Live leaderboard** — ranked by total profit at any point during the game
- **ANSI colour output** — colour-coded prices, messages, and stats in any modern terminal
- **No dependencies** — stdlib only (`random`, `time`, `os`, `dataclasses`)

---

## Requirements

Python 3.7+

---

## Usage

```bash
git clone https://github.com/Shipovmax/auction
cd auction
python main.py
```

You will be prompted for your name, then the game starts.

**Controls during a round:**

| Input | Action |
|-------|--------|
| `1` | Buy the current lot at the current price |
| `2` | Wait — price drops by 1,000 ₽, AI acts |
| `3` | Show the leaderboard |
| `4` | Skip the round |

---

## Project Structure

```
auction/
└── main.py    # Everything: models, game logic, AI, rendering
```

---

## Author

- GitHub: [Shipovmax](https://github.com/Shipovmax)
- Email: shipov.max@icloud.com
