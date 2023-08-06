from .._core import is_convex
import numpy as np

small_convex_polygon = [[0, 0], [0, 1], [1, 1], [1, 0]]
large_convex_polygon = np.array(
    [(np.cos(a), np.sin(a)) for a in np.linspace(0, 2 * np.pi, 200, False)]
)
small_clockwise_convex_polygon = [[0, 0], [1, 0], [1, 1], [0, 1]]
convex_polygon_with_180deg_edge = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1]]

not_convex_polygon = [(0, 0), (1, 1), (0, 1), (1, 0)]


def test_convex():
    """Test with convex polygon."""
    assert is_convex(small_convex_polygon)
    assert is_convex(small_clockwise_convex_polygon)
    assert is_convex(large_convex_polygon)
    assert is_convex(convex_polygon_with_180deg_edge)


def test_notconvex():
    """Test with nonconvex polygon."""
    assert not is_convex(not_convex_polygon)
