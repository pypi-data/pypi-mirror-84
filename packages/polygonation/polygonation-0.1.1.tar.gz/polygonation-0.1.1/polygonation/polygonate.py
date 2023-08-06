"""
Module to turn a set of points into a set of nonoverlapping polygons.

Done by identifying the removable edges, and then removing one of them.
Rinse-repeat until no further edges can be removed.

Not optimized or anything. For example, all candidiates are recalculated
after removing an edge.
"""

import numpy as np
from scipy.spatial import Delaunay
from typing import Iterable


def is_convex(polygon: Iterable) -> bool:
    """
    Evaluates if a polygon is convex or not.

    Parameters
    ----------
    polygon
        Iterable of points (x, y) in order as they appear in the polygon.

    Returns
    -------
    True if the polynomial is convex, False if it is not.

    Notes
    -----
    Implementation: convexness is checked by 'driving around the polygon'.
    Convex means 'never steer to the left' or 'never steer to the right'. No
    checks are done for complex cases such as self-intersecting polygons etc.
    """
    polygon = np.array(polygon)
    if len(polygon) < 3:  # Check for too few points
        return False
    orientation = 0
    for p1, p2, p3 in zip(*[np.roll(polygon, i, axis=0) for i in range(3)]):
        dxa, dya = p2 - p1
        dxb, dyb = p3 - p2
        cross = dxa * dyb - dya * dxb
        if not (-1e-5 < cross < 1e-5):
            if orientation == 0:
                orientation = np.sign(cross)
            elif orientation != np.sign(cross):
                return False
    return True


class Polygonate:
    """
    Tessellate a set of points with a set of non-overlapping polygons.

    Parameters
    ----------
    points
        Iterable of points (x, y).
    pickedge : {'actue', 'long', 'round'}, optional
        'acute' to remove the most acute angle first;
        'long' to remove the longest edge first;
        'round' to remove edge to create polygon with roundest corners.
    convex : bool, optional
        True if polygons must be convex (default).

    Attributes
    ----------
    points : ndarray of (x, y)
        Coordinates of input points.
    shapes : ndarray of ndarray of ints
        Indices of points forming the vertices of the calculated shapes.
    neighbors : ndarray of ndarray of ints
        Indices of shapes that are share at least 1 edge with the given shape.

    """

    def __init__(self, points: Iterable, *, pickedge: str = "", convex: bool = True):
        self._points = np.array(points)
        self.__convex = convex
        (
            self._shapes,
            self._neighbors,
            self._descendent_of_simplex,
        ) = self.__polygonation(pickedge)

    @property
    def points(self):
        """The (x, y) coordinates of the points."""
        return self._points

    @property
    def shapes(self):
        """The point-indices of the vertices of each shape."""
        return self._shapes

    @property
    def neighbors(self):
        """The neighbors of each shape."""
        return self._neighbors

    def __polygonation(self, pickedge):
        self._delaunay = Delaunay(self._points)
        shapes = self._delaunay.simplices.tolist()
        descendent_of_simplex = np.arange(len(shapes))
        neighbors = [
            [si for si in neighbors if si != -1]
            for neighbors in self._delaunay.neighbors
        ]

        if pickedge.startswith("long"):

            def f(cands):
                return np.argmax([cand["length"] for cand in cands])

        elif pickedge.startswith("round"):

            def f(cands):
                return np.argmin([cand["error"] for cand in cands])

        else:

            def f(cands):
                return np.argmin([cand["angles_before"].min() for cand in cands])

        def melt(
            si1, si2, shape3
        ):  # remove shapes with indices si1 and si2. Add shape with vertices shape3.
            nonlocal shapes, neighbors, descendent_of_simplex
            if si1 > si2:
                si1, si2 = si2, si1  # so that always si1 < si2
            shapes.pop(si2)
            shapes.pop(si1)
            si3 = len(shapes)
            shapes.append(shape3)
            nei3 = [*neighbors.pop(si2), *neighbors.pop(si1)]
            nei3 = [si for si in nei3 if si != si1 and si != si2]
            neighbors.append(nei3)

            def new_si(si):
                if si == si1 or si == si2:
                    return si3
                if si < si1:
                    return si
                if si < si2:
                    return si - 1
                return si - 2

            neighbors = [[new_si(si) for si in neighbors] for neighbors in neighbors]
            descendent_of_simplex = [new_si(si) for si in descendent_of_simplex]

        while True:
            cands = self._candidates(shapes, neighbors)
            if len(cands) == 0:
                break
            # Find which one to remove.
            picked = cands[f(cands)]
            melt(*picked["si"], picked["shape3"])

        return shapes, neighbors, descendent_of_simplex

    def _candidates(self, shapes: Iterable, neighbors: Iterable):
        """
        Find the edges that could be removed. Also store additional information,
        such as edge length and existing angles.
        """

        def prepshape(
            shape, edge
        ):  # rotate/flip shape so, that edge[0] is at start and edge[1] is at end.
            while len(np.intersect1d(shape[0:2], edge)) != 2:
                shape = np.roll(shape, 1)
            shape = np.roll(
                shape, -1
            )  # one edge vertice at start, the other at the end.
            if shape[0] == edge[1]:
                shape = np.flip(shape)  # edge[0] is at beginning, edge[1] is at end
            return shape

        def vec(*vi):
            return self._points[vi[1]] - self._points[vi[0]]

        def angle(vecA, vecB):
            cosangle = np.dot(vecA, vecB) / (
                np.linalg.norm(vecA) * np.linalg.norm(vecB)
            )
            return np.arccos(np.clip(cosangle, -1, 1))

        def PolyArea(vi):
            x, y = self._points[vi, 0], self._points[vi, 1]
            return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        candidates = []
        for si1, neighbors in enumerate(neighbors):
            shape1 = shapes[si1]
            for si2 in neighbors:
                if si1 > si2:
                    continue  # only add each edge once
                shape2 = shapes[si2]
                # Find vertices of shared edge.
                edge = np.intersect1d(shape1, shape2)
                if len(edge) != 2:
                    continue
                # Prepare by putting edge vertice 0 (1) at position 0 (-1) in each shape
                shape1, shape2 = prepshape(shape1, edge), prepshape(shape2, edge)
                # Get candidate-polygon
                shape3 = [*shape1[:-1], *shape2[::-1][:-1]]
                if self.__convex and not is_convex(self._points[shape3]):
                    continue
                # Add characteristics.
                edgevec = vec(*edge)  # pointing 0->1
                # Vectors pointing along the edges, starting at where edge is.
                vecs = [
                    [vec(*vi) for vi in [shape1[:2], shape2[:2]]],
                    [vec(*vi) for vi in [shape1[-2:], shape2[-2:]]],
                ]
                angles = np.array(
                    [[angle(edgevec, v) for v in vec] for vec in vecs]
                )  # angles at corner 0, angles at corner 1
                candidates.append(
                    {
                        "edge": [*edge],
                        "si": [si1, si2],
                        "shape3": shape3,
                        "length": np.linalg.norm(edgevec),
                        "angles_before": angles,
                        "angles_after": angles.sum(axis=1),
                        "error": np.abs(
                            angles.sum(axis=1) - (np.pi * (1 - 2 / len(shape3)))
                        ).mean(),
                    }
                )
        return candidates

    def find_shape(self, point: Iterable) -> int:
        """
        Returns index of shape that contains the speficied `point`.

        Parameters
        ----------
        point
            Coordinates (x, y) of point.
        """
        sim = self._delaunay.find_simplex(point)
        if sim > -1:
            return self._descendent_of_simplex[sim]
        return -1
