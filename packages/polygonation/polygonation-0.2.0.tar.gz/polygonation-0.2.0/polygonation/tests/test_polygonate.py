from .._core import Polygonate
import numpy as np
from scipy.spatial import Delaunay


def test_convex():
    """Set of points resulting in single polygon regardless of convexness-requirement."""
    points = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    pg = Polygonate(points)
    assert len(pg.shapes) == 1
    pg = Polygonate(points, convex=False)
    assert len(pg.shapes) == 1


def test_notconvex():
    """Set of points resulting in multiple polygons in both cases."""
    points = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.6]])
    pg = Polygonate(points)
    assert len(pg.shapes) == 3
    pg = Polygonate(points, convex=False)
    assert len(pg.shapes) == 2


def test_correctshape():
    """Check if correct shape is identified for the container of a point."""

    def check_correct_shape(pg, p):
        s = pg.find_shape(p)
        if s > -1:  # Shape is found. p should be in one of its Delaunay triangles.
            delaunay = Delaunay(points[pg.shapes[s]])
            assert delaunay.find_simplex(p) >= 0

    points = np.random.rand(50, 2)
    checkpoints = np.random.rand(10, 2)

    pg = Polygonate(points)
    for p in checkpoints:
        check_correct_shape(pg, p)
    pg = Polygonate(points, convex=False)
    for p in checkpoints:
        check_correct_shape(pg, p)
