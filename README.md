# python-ataxx: A Python library for the board game Ataxx

## About
python-ataxx is written in Python 3 and supports basic features such as move generation, move validation, engine communication, and board printing.

## Usage
```Python3
>>> import ataxx
>>> board = ataxx.Board()
>>> board.makemove(ataxx.parse_san("g2"))
>>> board.makemove(ataxx.parse_san("a7a5"))
>>> board.get_fen()
'6o/7/o6/7/7/6x/o5x x'
```

## Features
* Printing the board
```Python3
>>> board = ataxx.Board()
>>> print(board)
  a b c d e f g
 ╔═╦═╦═╦═╦═╦═╦═╗
7║X║ ║ ║ ║ ║ ║O║7
 ╠═╬═╬═╬═╬═╬═╬═╣
6║ ║ ║ ║ ║ ║ ║ ║6
 ╠═╬═╬═╬═╬═╬═╬═╣
5║ ║ ║ ║ ║ ║ ║ ║5
 ╠═╬═╬═╬═╬═╬═╬═╣
4║ ║ ║ ║ ║ ║ ║ ║4
 ╠═╬═╬═╬═╬═╬═╬═╣
3║ ║ ║ ║ ║ ║ ║ ║3
 ╠═╬═╬═╬═╬═╬═╬═╣
2║ ║ ║ ║ ║ ║ ║ ║2
 ╠═╬═╬═╬═╬═╬═╬═╣
1║O║ ║ ║ ║ ║ ║X║1
 ╚═╩═╩═╩═╩═╩═╩═╝
  a b c d e f g
Turn: X
```

* FEN parsing
```Python3
>>> board = ataxx.Board("startpos")
>>> board = ataxx.Board("x5o/7/2-1-2/7/2-1-2/7/o5x x")
```

* Result detection
```Python3
>>> board.gameover()
True
>>> board.fifty_move_draw()
False
>>> board.max_length_draw()
False
```

* Communication with UAI compatible engines
```Python3
>>> import ataxx.uai
>>> engine = ataxx.uai.Engine("tiktaxx")
>>> engine.uai()
>>> engine.isready()
>>> engine.name
'Tiktaxx'
>>> board = ataxx.Board()
>>> engine.position(board)
>>> bestmove, ponder = engine.go(movetime=1000)
>>> engine.go(movetime=1000)
('a7b5', None)
>>> engine.quit()
```

* Simple players
```Python3
>>> import ataxx.players
>>> board = ataxx.Board()
>>> ataxx.players.greedy(board)
<ataxx.Move object at 0x7f7747e28860>
```
