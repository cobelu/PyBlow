import click
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv


@click.command()
@click.option('-a', prompt='Size', type=float)
@click.option('-b', prompt='"Egg-iness"', type=float)
@click.option('--n_curve', prompt='Number of points', type=int)
@click.option('--n_arc', prompt='Number of points', type=int)
def pyblow(a: float, b: float, n_curve: int, n_arc: int):
    theta = np.linspace(0, 2 * np.pi, n_curve)
    r = a * (1 + b * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    plt.plot(x, y)
    plt.title("Plotting NumPy Arrays")
    plt.show()

    # phi = np.linspace(0, np.pi, n_arc)
    # dx = np.gradient(x)
    # dy = np.gradient(y)
    #
    # norm = np.sqrt(dx ** 2 + dy ** 2)
    # nx = -dy / norm
    # ny = dx / norm
    #
    # X = np.zeros((n_curve, n_arc))
    # Y = np.zeros((n_curve, n_arc))
    # Z = np.zeros((n_curve, n_arc))
    #
    # for i in range(n_curve):
    #     R = r[i]
    #     X[i] = x[i] + nx[i] * R * np.cos(phi)
    #     Y[i] = y[i] + ny[i] * R * np.cos(phi)
    #     Z[i] = R * np.sin(phi)
    #
    # vertices = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
    # write_binary_stl("example.stl", vertices)

    return


def write_binary_stl(filename, vertices):
    point_cloud = pv.PolyData(vertices)
    mesh = point_cloud.reconstruct_surface()
    mesh.save(filename)


if __name__ == '__main__':
    pyblow()
