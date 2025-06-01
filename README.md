# Checkers Game

A Checkers game for 2 players built using **Python** and **Pygame**, 
featuring classical 8x8 board, piece movement, king promotion, move highlighting, and sound effects.

![screenshot](resources/board2.png)

---

## Features

- Two-player local gameplay (server - client)
- Visual highlighting of legal moves
- Piece promotion to king
- Sound effects on moves
- Custom piece and board graphics
- Capture obligation (you need to capture an opponent's piece if possible)
- Handling if the one player quits

---

## Project Structure
```
 Checkers
  ├── resources
  │   ├── board2.png
  │   ├── king_black.png
  │   ├── king_white.png
  │   └── move_sound.wav
  │   
  ├── board.py
  ├── forwarding.py
  ├── graphics.py
  ├── piece.py
  ├── server.py
  ├── checkers.py
  ├── game.py
  ├── network.py
  ├── square.py
  └── README.md
```

## What to do to run the game?
#### 1st player [server]:
     1. python checkers.py
     2. type: 'h'
     3. wait for the second player (client) to connect

#### 2nd player [client]:
     1. python checkers.py
     2. type: 'j'
     3. type: '127.0.0.1' (ip of server)

## Requirements:
- Python 3.7+
- Pygame library installed

## Visual Demonstration:
##### start of a game
![screenshot](screenshots/start_a_game.png)

##### after clicking a piece (highlighting possible moves)
![screenshot](screenshots/possible_moves.png)

##### after clicking a piece (possible to capture a piece)
![screenshot](screenshots/capture_piece.png)

##### multiple capture + king transformation
![screenshot](screenshots/multiple_capture_1.png)
![screenshot](screenshots/multiple_capture_2.png)
![screenshot](screenshots/multiple_capture_3_king.png)

##### capture obligation (piece 2 can't move, because piece 1 can capture a piece)
![screenshot](screenshots/capture_obligation.png)

##### king movement
![screenshot](screenshots/king_capture.png)

##### Winner message
![screenshot](screenshots/winner_message.png)

##### Opponent quit message
![screenshot](screenshots/opponent_quit_message.png)


