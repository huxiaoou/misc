if __name__ == "__main__":
    import os
    import sys
    from packages.pkg_cus import add

    print("\nsys.path:")
    for path in sys.path:
        print(path)

    print("Current working directory:", os.getcwd())
    print("Addition of 3 and 5:", add(3, 5))
