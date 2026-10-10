# Python Games Interface

A Tkinter menu for launching several small Python games from one desktop window.

<img src="../docs/images/python-games-menu.png" width="360" alt="Python games launcher with six game buttons">

## Included games

- Tic Tac Toe
- Snake
- Minesweeper
- 2048 on a 5 × 5 board
- Flappy Bird
- Memory Match

The folder also contains a typing speed test and a leaderboard interface. Games that record scores use `leaderboard_core.py` and store their data in `scores.json`.

## Run

With a Python installation that includes Tkinter, open a terminal in this folder and run:

```sh
python game_menu.py
```

The menu launches each game as a separate Python process. You can also run an individual game file directly. The leaderboard creates `scores.json` locally; it is ignored by Git so personal scores are not committed.
