
import math
import time
import msvcrt

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


def draw_shapes(width=36, height=14):
    canvas = [[" " for _ in range(width)] for _ in range(height)]

    # Draw rectangle
    for x in range(2, 15):
        canvas[2][x] = "─"
        canvas[7][x] = "─"

    for y in range(3, 7):
        canvas[y][2] = "│"
        canvas[y][14] = "│"

    for x, y, c in [
        (2, 2, "┌"), (14, 2, "┐"),
        (2, 7, "└"), (14, 7, "┘"),
    ]:
        canvas[y][x] = c

    # Draw circle
    cx, cy = 25, 5
    rx, ry = 7, 4

    for i in range(360):
        angle = math.radians(i)
        x = round(cx + rx * math.cos(angle))
        y = round(cy + ry * math.sin(angle))
        canvas[y][x] = "●"

    return Text("\n".join("".join(row) for row in canvas))


def main():
    layout = Layout()
    layout.split_row(
        Layout(name="console", ratio=1),
        Layout(name="graphics", ratio=1),
    )

    messages = []

    with Live(layout, screen=True, refresh_per_second=4):
        i = 0

        while True:
            # Check keyboard input without blocking
            if msvcrt.kbhit():
                key = msvcrt.getwch()

                if key.lower() == "q":
                    break

            messages.append(f"[INFO] Iteration {i}")

            layout["console"].update(
                Panel("\n".join(messages[-15:]), title="Console")
            )
            layout["graphics"].update(
                Panel(draw_shapes(), title="Graphics")
            )

            i += 1
            time.sleep(0.2)

    # Printed after Live exits and restores the terminal
    print("User pressed 'q'. Program terminated.")


if __name__ == "__main__":
    main()
