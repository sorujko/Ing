import streamlit as st
import random
import numpy as np
st.set_page_config(layout='centered' , page_title="Covid")
# Constants
CANVAS_SIZE = 400
RECT_SIZE = 20
COLOR_BLUE = "blue"
COLOR_GREEN = "green"
COLOR_RED = "red"
COLOR_YELLOW = "yellow"
COLOR_DEFAULT = "white"
NEIGHBOR_OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Neighboring rectangle offsets

def update_canvas(rectangles, canvas, scoreboards):
    # Find the colorful rectangles
    colorful_rectangles = []
    for x in range(len(rectangles)):
        for y in range(len(rectangles[x])):
            if rectangles[x][y]["color"] != COLOR_DEFAULT:
                colorful_rectangles.append((x, y))

    # Shuffle the colorful rectangles to randomize the order
    random.shuffle(colorful_rectangles)

    # Update the neighbors' colors
    for position in colorful_rectangles:
        x, y = position
        attacker = rectangles[x][y]
        color = attacker["color"]

        if not attacker.get("changed", False):  # Check if the attacker's color has been changed
            for dx, dy in NEIGHBOR_OFFSETS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < CANVAS_SIZE // RECT_SIZE and 0 <= ny < CANVAS_SIZE // RECT_SIZE:
                    defender = rectangles[nx][ny]
                    if defender["color"] == COLOR_DEFAULT and random.random() < 0.1:
                        defender["color"] = color
                    elif (
                        defender["color"] != COLOR_DEFAULT
                        and defender["color"] != color
                        and not defender.get("changed", False)  # Check if defender's color has been changed
                    ):
                        # Battle between attacker and defender
                        if random.random() < 0.5:
                            defender["color"] = color
                            defender["changed"] = True  # Set the "changed" flag for the defender

        attacker["changed"] = True  # Set the "changed" flag for the attacker

    # Clear the "changed" flag for cells that transitioned from white to color
    for x in range(len(rectangles)):
        for y in range(len(rectangles[x])):
            cell = rectangles[x][y]
            if "changed" in cell and cell["color"] != COLOR_DEFAULT:
                cell.pop("changed")

    # Update the scoreboards
    scores = {}
    for color in scoreboards:
        count = sum(1 for x in range(len(rectangles)) for y in range(len(rectangles[x])) if rectangles[x][y]["color"] == color)
        scores[color] = count
        scoreboards[color].text(f"{color}: {count}")

    # Check if three colors have a count of 0
    if len([count for count in scores.values() if count == 0]) >= 3:
        st.text("Three colors have a count of 0. Stopping the program.")
        canvas.image(draw_canvas(rectangles),)
        st.stop()

    # Update the canvas
    canvas.image(draw_canvas(rectangles),use_column_width=False)

def main():
    st.title("Cellular Automaton in Streamlit")

    # Create rectangles and store them in a grid-like structure
    rectangles = []
    for x in range(CANVAS_SIZE // RECT_SIZE):
        row = []
        for y in range(CANVAS_SIZE // RECT_SIZE):
            row.append({"color": COLOR_DEFAULT, "position": (x, y)})
        rectangles.append(row)

    # Set the initial colors for each corner
    corners = [
        (0, 0, COLOR_GREEN),
        (CANVAS_SIZE // RECT_SIZE - 1, 0, COLOR_RED),
        (0, CANVAS_SIZE // RECT_SIZE - 1, COLOR_YELLOW),
        (CANVAS_SIZE // RECT_SIZE - 1, CANVAS_SIZE // RECT_SIZE - 1, COLOR_BLUE),
    ]
    for corner in corners:
        x, y, color = corner
        initial_rect = rectangles[x][y]
        initial_rect["color"] = color

    # Create a canvas
    canvas = st.empty()

    # Create scoreboards to track the number of cells with each color
    scoreboards = [COLOR_GREEN, COLOR_RED, COLOR_YELLOW, COLOR_BLUE]
    scoreboard_counts = {color: st.empty() for color in scoreboards}
    for color in scoreboards:
        scoreboard_counts[color].text(f"{color}: 0")

    while True:
        update_canvas(rectangles, canvas, scoreboard_counts)

@st.cache_data
def draw_canvas(rectangles):
    canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)

    for x in range(len(rectangles)):
        for y in range(len(rectangles[x])):
            color = rectangles[x][y]["color"]
            color_rgb = (255, 255, 255)  # Default background color
            if color == COLOR_GREEN:
                color_rgb = (0, 255, 0)
            elif color == COLOR_RED:
                color_rgb = (255, 0, 0)
            elif color == COLOR_YELLOW:
                color_rgb = (255, 255, 0)
            elif color == COLOR_BLUE:
                color_rgb = (0, 0, 255)
            canvas[x * RECT_SIZE:(x + 1) * RECT_SIZE, y * RECT_SIZE:(y + 1) * RECT_SIZE] = color_rgb

    return canvas

if __name__ == "__main__":
    main()
