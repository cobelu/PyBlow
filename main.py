import click
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv


@click.command()
@click.option("--length", prompt="Sheet length (inches)", type=float, default=96.0)
@click.option("--width", prompt="Sheet width (inches)", type=float, default=48.0)
@click.option("--height", prompt="Bubble height (inches)", type=float, default=12.0)
@click.option("--resolution", prompt="Mesh resolution (points per side)", type=int, default=50)
@click.option("--output", prompt="Output filename", type=str, default="bubble.stl")
def pyblow(length: float, width: float, height: float, resolution: int, output: str):
    """
    Generate a 3D mesh of a blown acrylic bubble.

    Models a rectangular acrylic sheet that has been heated and blown into a bubble shape.
    The edges remain flat (z=0) and the center rises to the specified height.
    """
    print(f"Generating bubble: {length}\" x {width}\" x {height}\" high")
    print(f"Mesh resolution: {resolution} x {resolution}")

    # Generate the bubble mesh
    vertices, faces = generate_bubble_mesh(length, width, height, resolution)

    # Visualize (optional)
    # plot_3D(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    # Write to STL
    write_mesh_stl(output, vertices, faces)
    print(f"STL file written to: {output}")

    return


def generate_bubble_mesh(length: float, width: float, height: float, resolution: int):
    """
    Generate a structured mesh for a blown acrylic bubble.

    Uses an ellipsoidal cap model where:
    - The base is a rectangle (length x width)
    - The height follows an ellipsoidal profile
    - Edges are at z=0 (flat/clamped)

    Args:
        length: Length of the acrylic sheet (X direction)
        width: Width of the acrylic sheet (Y direction)
        height: Maximum height of the bubble at center
        resolution: Number of grid points along each dimension

    Returns:
        vertices: Nx3 array of vertex coordinates
        faces: Mx3 array of triangle face indices
    """
    # Create a grid of points on the XY plane
    x = np.linspace(-length / 2, length / 2, resolution)
    y = np.linspace(-width / 2, width / 2, resolution)
    X, Y = np.meshgrid(x, y)

    # Calculate Z height using ellipsoidal cap formula
    # For a point (x, y), calculate normalized distance from center
    # z = h * sqrt(1 - (x/a)^2 - (y/b)^2) for points inside the ellipse

    a = length / 2  # Semi-major axis in X
    b = width / 2   # Semi-major axis in Y

    # Normalized squared distance from center
    norm_dist_sq = (X / a) ** 2 + (Y / b) ** 2

    # Calculate height - ellipsoidal cap
    # Only positive values (above the XY plane)
    Z = np.zeros_like(X)
    inside_mask = norm_dist_sq <= 1.0
    Z[inside_mask] = height * np.sqrt(1 - norm_dist_sq[inside_mask])

    # Flatten the grid into a vertex list
    vertices = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

    # Generate triangle faces for the structured grid
    faces = []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            # Each grid cell creates two triangles
            # Vertex indices in the flattened array
            v0 = i * resolution + j
            v1 = i * resolution + (j + 1)
            v2 = (i + 1) * resolution + j
            v3 = (i + 1) * resolution + (j + 1)

            # Two triangles per quad
            faces.append([v0, v1, v2])
            faces.append([v1, v3, v2])

    faces = np.array(faces)

    return vertices, faces


def plot_3D(x, y, z):
    """Visualize the 3D mesh as a scatter plot."""
    ax = plt.figure().add_subplot(projection="3d")
    ax.scatter(x, y, z, c=z, cmap='viridis', s=1)
    ax.set_xlabel('X (inches)')
    ax.set_ylabel('Y (inches)')
    ax.set_zlabel('Z (inches)')
    ax.set_title('Blown Acrylic Bubble')
    plt.show()


def write_mesh_stl(filename: str, vertices: np.ndarray, faces: np.ndarray):
    """
    Write a mesh to an STL file using PyVista.

    Args:
        filename: Output STL filename
        vertices: Nx3 array of vertex coordinates
        faces: Mx3 array of triangle face indices
    """
    # PyVista expects faces in format: [3, v0, v1, v2, 3, v3, v4, v5, ...]
    # where the first number is the count of vertices per face
    pv_faces = np.column_stack((np.full(len(faces), 3), faces)).ravel()

    # Create PyVista mesh
    mesh = pv.PolyData(vertices, pv_faces)

    # Save to STL
    mesh.save(filename)


if __name__ == "__main__":
    pyblow()
