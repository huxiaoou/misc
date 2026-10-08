from .utils import print_utils_info
import os


def add(a: int | float, b: int | float) -> int | float:
    print("Current working directory, called in add:", os.getcwd())
    return a + b


if __name__ == "__main__":
    import sys

    print("\nsys.path:")
    for path in sys.path[0:1]:
        print(path)
    print("Current working directory, called in pkg_cus as main:", os.getcwd())
    print("Addition of 3 and 5:", add(3, 5))
    
    print_utils_info()
