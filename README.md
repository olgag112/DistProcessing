# Checkers Game

A Checkers game for 2 players built using **Python** and **Pygame**, 
featuring classical 8x8 board, piece movement, king promotion, move highlighting, and sound effects.


<img src="resources/board2.png" alt="Demo" width="400"/>

---
## Table of Contents
1. [Game Features](##Features)
2. [Project Structure](## Project Structure)
3. [Concurrency Methods](##concurrent-programming-methods)
4. [Libraries & Frameworks](##external-librariesframeworks)
5. [Screenshots](##screenshots)
6. [Setup & Installation](##setup--installation)
7. [How to Play](##ow-to-play)
8. [Group Member Contributions](##group-member-contributions)
9. [License](##license)


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
<img src="screenshots/start_a_game.png" alt="Demo" width="400"/>

##### after clicking a piece (highlighting possible moves)
<img src="screenshots/possible_moves.png" alt="Demo" width="400"/>

##### after clicking a piece (possible to capture a piece)
<img src="screenshots/capture_piece.png" alt="Demo" width="400"/>

##### multiple capture + king transformation
<p float="left">
 <img src="screenshots/multiple_capture_1.png" alt="Demo" width="300"/>
 <img src="screenshots/multiple_capture_2.png" alt="Demo" width="300"/>
 <img src="screenshots/multiple_capture_3_king.png" alt="Demo" width="300"/>
</p>

##### capture obligation (piece 2 can't move, because piece 1 can capture a piece)
<img src="screenshots/capture_obligation.png" alt="Demo" width="400"/>

##### king movement
<img src="screenshots/king_capture.png" alt="Demo" width="400"/>

##### Winner message
<img src="screenshots/winner_message.png" alt="Demo" width="400"/>

##### Opponent quit message
<img src="screenshots/opponent_quit_message.png" alt="Demo" width="400"/>


