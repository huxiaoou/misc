import matplotlib.pyplot as plt
import numpy as np


def bezier(t: np.ndarray | float, start: np.ndarray, mid: np.ndarray, end: np.ndarray) -> np.ndarray:
    """Calculate a point on a quadratic Bezier curve.

    Args:
        t (np.ndarray): A parameter between 0 and 1 indicating the position along the curve.
        start (np.ndarray): The starting point of the curve.
        mid (np.ndarray): The control point of the curve.
        end (np.ndarray): The ending point of the curve.

    Returns:
        np.ndarray: The calculated point on the Bezier curve at parameter t.
    """
    return (1 - t) ** 2 * start + 2 * (1 - t) * t * mid + t**2 * end


if __name__ == "__main__":
    # Define control points
    start_point = np.array([3.14, -1]).reshape(2, 1)
    end_point = np.array([5, 2]).reshape(2, 1)
    control_scale = -0.3
    distance = np.linalg.norm(end_point - start_point)

    hd = end_point - start_point
    hd = hd / np.linalg.norm(hd)
    vd = np.array([-hd[1], hd[0]]).reshape(2, 1)
    control_point = control_scale * distance * vd + (start_point + end_point) / 2
    peak_point = bezier(0.5, start_point, control_point, end_point)

    # Generate t values
    t_values = np.linspace(0, 1, 100)

    # Calculate Bezier curve points
    bp = bezier(t_values, start_point, control_point, end_point)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(*bp, label="Bezier Curve", color="blue")
    plt.plot(*start_point, "ro", label="Start Point")
    plt.plot(*control_point, "go", label="Control Point")
    plt.plot(*end_point, "bo", label="End Point")
    plt.plot(*peak_point, "mo", label="Peak Point")
    plt.title("Quadratic Bezier Curve")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.grid()
    plt.axis("equal")
    plt.show()
