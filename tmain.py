import msvcrt

print("Press 'q' to quit, any other key to print its value:")

while True:
    # Check if a key has been pressed
    if msvcrt.kbhit():
        # Get the character. getch() returns bytes, so decode to utf-8.
        char_bytes = msvcrt.getch()
        if char_bytes in (b'\x00', b'\xe0'):
            char_bytes = msvcrt.getch()
            if char_bytes == b'H':
                print("Up")
            elif char_bytes == b'P':
                print("Down")
            elif char_bytes == b'K':
                print("Left")
            elif char_bytes == b'M':
                print("Right")
            continue

        key = char_bytes.decode("utf-8").lower()
        print(f"Pressed: {key}")
        if key == 'q':
            break

