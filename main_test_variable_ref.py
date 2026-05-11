def lstrip_sharp(a: str) -> str:
    print(f"Before a={a}")
    a = a.lstrip("#")
    print(f"After  a={a}")
    return a


def change(d: dict[str, int], key: str) -> dict[str, int]:
    print(f"Before d={d}")
    d.pop(key, None)
    print(f"After  d={d}")
    return d


if __name__ == "__main__":
    x = "#ff00ff"
    lstrip_sharp(x)
    print(f"After strip x={x}")

    y = dict(m=1, n=2, p=3)
    change(y, "n")
    print(f"After change y={y}")
