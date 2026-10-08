if __name__ == "__main__":
    import os
    import sys
    from packages.app import add, print_utils_info

    print("\nsys.path:")
    for path in sys.path[0:1]:
        print(path)

    print("Current working directory, called in main:", os.getcwd())
    print("Addition of 3 and 5:", add(3, 5))
    print_utils_info()
