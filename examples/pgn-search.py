import ataxx
import ataxx.pgn

def main():
    """
    Search games.pgn for the specified player
    """
    target = "Player 2"
    for game in ataxx.pgn.GameIterator("games.pgn"):
        if target in [game.headers["Black"], game.headers["White"]]:
            print(game)
            input()

if __name__ == "__main__":
    main()
