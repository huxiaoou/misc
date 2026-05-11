import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh rate (ms)

    # Initial snake
    sh, sw = stdscr.getmaxyx()
    snake = [[sh//2, sw//2]]
    direction = curses.KEY_RIGHT

    # Food
    food = [random.randint(1, sh-2), random.randint(1, sw-2)]

    while True:
        # Input
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        # Move snake head
        head = snake[0].copy()
        if direction == curses.KEY_UP:    head[0] -= 1
        elif direction == curses.KEY_DOWN: head[0] += 1
        elif direction == curses.KEY_LEFT: head[1] -= 1
        elif direction == curses.KEY_RIGHT: head[1] += 1

        # Check collisions
        if (head[0] in [0, sh-1] or head[1] in [0, sw-1] or head in snake):
            break  # Game over

        snake.insert(0, head)

        # Eat food
        if head == food:
            food = [random.randint(1, sh-2), random.randint(1, sw-2)]
        else:
            snake.pop()

        # Draw
        stdscr.clear()
        stdscr.addstr(food[0], food[1], '🍎')  # Or '*' if emoji not supported
        for i, (y, x) in enumerate(snake):
            stdscr.addstr(y, x, '🐍' if i == 0 else '●')

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)