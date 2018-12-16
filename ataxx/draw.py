import ataxx
from PIL import Image, ImageDraw, ImageFont

BACKGROUND_COLOUR = (50, 50, 50)
HIGHLIGHT_SQUARE  = (146, 177, 102)
LIGHT_SQUARE      = (220, 230, 230)
DARK_SQUARE       = (140, 160, 170)
WHITE_PIECE       = (235, 235, 235)
BLACK_PIECE       = (20, 20, 20)

def board(board, width, height, highlights=[], coordinates=False):
    """
    Return a PIL.Image.Image for the current board position
    """

    image = Image.new("RGB", (width, height), BACKGROUND_COLOUR)
    draw = ImageDraw.Draw(image)
    font = None

    # Load a font if required
    if coordinates:
        try:
            font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 16)
        except IOError:
            font = ImageFont.load_default()
        finally:
            if not font:
                coordinates = False

    grid_width  = width/board.w
    grid_height = height/board.h

    # Gap between the piece and the square edge
    gap_x = int(0.05*grid_width)
    gap_y = int(0.05*grid_height)

    for x in range(board.w):
        for y in range(board.h):
            piece = board.get(x, board.h-y-1)

            # Don't draw anything over gaps
            if piece == ataxx.GAP:
                continue

            # (x1, y1) (x2, y1)
            # (x1, y2) (x2, y2)
            x1, x2 = int(x*grid_width),  int((x+1)*grid_width)
            y1, y2 = int(y*grid_height), int((y+1)*grid_height)

            # Grid coordinates
            top_left     = (x1, y1)
            bottom_right = (x2, y2)

            # Piece coordinates
            top_left_piece     = (x1+gap_x, y1+gap_y)
            bottom_right_piece = (x2-gap_x, y2-gap_y)

            # Draw -- Checkerboard pattern
            is_light = (x + y)%2
            if is_light:
                draw.rectangle([top_left, bottom_right], fill=LIGHT_SQUARE, outline="black")
            else:
                draw.rectangle([top_left, bottom_right], fill=DARK_SQUARE, outline="black")

            # Draw -- Square highlights
            if (x, board.h-y-1) in highlights:
                draw.rectangle([top_left, bottom_right], fill=HIGHLIGHT_SQUARE, outline="black")

            # Draw -- Black piece
            if piece == ataxx.BLACK:
                draw.ellipse([top_left_piece, bottom_right_piece], fill=BLACK_PIECE, outline="black")
            # Draw -- white piece
            elif piece == ataxx.WHITE:
                draw.ellipse([top_left_piece, bottom_right_piece], fill=WHITE_PIECE, outline="black")

            # Draw -- Coordinates
            if coordinates and font is not None:
                coordinate = chr(x+ord("a")) + chr(board.h - y + ord("1") - 1)
                draw.text((top_left[0] + 2, top_left[1] + 2), coordinate, font=font, fill=(255,0,0,255))

    del draw
    return image

def fen(fen, width, height):
    """
    Return a PIL.Image.Image for the FEN specified
    """

    return board(ataxx.Board(fen), width, height)
