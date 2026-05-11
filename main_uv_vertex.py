import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class Vertex:
    x: float
    y: float
    z: float

    def div(self, radius: float) -> "Vertex":
        return Vertex(self.x / radius, self.y / radius, self.z / radius)

    def add(self, value: float) -> "Vertex":
        return Vertex(self.x + value, self.y + value, self.z + value)


@dataclass
class UV:
    u: float
    v: float


def main():
    sides: int = 6
    radius: float = 1.0
    vertices: list[Vertex] = []
    uvs: list[UV] = []
    for i in range(sides):
        angle = (2 * np.pi / sides) * i  # - np.pi / 6
        x = radius * np.cos(angle)
        y = 0.0
        z = radius * np.sin(angle)
        v = Vertex(x, y, z)
        vertices.append(v)
        print(v)

        vn = (v.div(radius).add(1)).div(2)
        uv = UV(vn.x, vn.z)
        uvs.append(uv)

    for uv in uvs:
        print(uv)

    xs, ys = [uv.u for uv in uvs] + [uvs[0].u], [uv.v for uv in uvs] + [uvs[0].v]
    plt.plot(xs, ys, "o-")
    plt.xlabel("u")
    plt.ylabel("v")
    plt.title("UV Coordinates")
    for x, y, i in zip(xs[:-1], ys[:-1], range(sides)):
        plt.text(x, y, f"P{i}=({x:.2f}, {y:.2f})", fontsize=8, ha="right", va="bottom")
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
