import argparse


def convert_hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


def create_colored_block(r: int, g: int, b: int, width: int, height: int) -> list[str]:
    """Create a string that represents a colored block in the terminal."""
    color_code = f"\033[48;2;{r};{g};{b}m"
    reset_code = "\033[0m"
    block_line = color_code + " " * max(width, 8) + reset_code
    block = [block_line] * height
    return block


def print_color_palette(hex_colors: list[str], block_width: int, block_height: int):
    """Print multiple colored blocks side by side."""

    blocks = []
    for hex_color in hex_colors:
        r, g, b = convert_hex_to_rgb(hex_color)
        block = create_colored_block(r, g, b, block_width, block_height)
        blocks.append(block)

    for i in range(block_height):
        line = ""
        for block in blocks:
            line += block[i]
        print(line)

    codes = (" " * max((block_width - 7), 1)).join(hex_colors)
    print(codes)


def print_palette(palettes: dict[str, list[str]], block_width: int, block_height: int):
    """Print multiple color palettes."""
    for name, colors in palettes.items():
        print(f"{name}:")
        print_color_palette(colors, block_width, block_height)
        print()
    return


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Display color palettes in the terminal.")
    parser.add_argument(
        "--width",
        type=int,
        default=10,
        help="Width of each color block (default: 10)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=3,
        help="Height of each color block (default: 3)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    palettes = {
        "Classic Tavern": ["#5d432c", "#c8782e", "#e8d8c9", "#2a4c3f", "#8a1b1b"],
        "Enchanted Forest": ["#1a3b2d", "#6a994e", "#4a3728", "#a2c5cc", "#9d4edd"],
        "Gothic Fortress": ["#2d2d2d", "#8a9597", "#4a6479", "#6d597a", "#b7410e"],
    }
    args = parse_arguments()
    print_palette(palettes=palettes, block_width=args.width, block_height=args.height)
