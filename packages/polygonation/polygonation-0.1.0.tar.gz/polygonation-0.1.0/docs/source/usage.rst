============
Sample usage
============

Getting started
---------------

Starting with importing relevant packages and creating some points in the plane:

.. ipython:: python

   import polygonation.polygonate as pg
   import numpy as np
   points = np.random.rand(20, 2)

We can then find a set of convex polygons that contain the given points, using
the ``Polygonate`` class. The ``.shapes`` attribute then gives the points in each polygon:

.. ipython:: python

   plgn1 = pg.Polygonate(points)
   plgn1.shapes


Using the ``is_convex`` function to verify that all polygons are indeed convex:

.. ipython:: python

   print([pg.is_convex(points[s]) for s in plgn1.shapes])


If we let go of the convexness criterium, we can find a smaller set of polygons:

.. ipython:: python

   plgn2 = pg.Polygonate(points, convex=False)
   plgn2.shapes

Here is a comparison of both polygonations:

.. ipython:: python
   :suppress:

    import matplotlib.pyplot as plt
    def plot1():
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        for i, (plgn, ax) in enumerate(zip([plgn1, plgn2], axes)):
            ax.plot(*points.T, 'ko') # points
            ax.triplot(*plgn.points.T, 'k:', alpha=0.3) # delaunay
            for shape in plgn.shapes:
                ax.plot(*plgn.points[[*shape, shape[0]]].T, 'b') # resulting polygons
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title('convex = ' + ['True', 'False'][i])
        fig.tight_layout()
        return fig

.. ipython:: python
    :suppress:

    @savefig plot1.png
    plot1();


Additional options
------------------

When creating a ``Polygonate`` object, the ``pickedge`` parameter controls which
edge is removed in each step. Here is a comparison with a larger set of points:

.. ipython:: python
    :suppress:

    points = np.random.rand(60, 2)
    def plot2(convex):
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        for i, j in np.ndindex(axes.shape):
            ax = axes[i, j]
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values(): s.set_visible(False)
            if i==0 and j<2: continue
            kwargs = {'alpha': 0.1} if i > 0 else {}
            ax.triplot(*points.T, 'k:', alpha=0.3)
        fig.suptitle(f'convex = {convex}')
        axes[0,0].set_title('points')
        axes[0,0].plot(*points.T, 'ko')
        axes[0,2].set_title('Delaunay grid')
        for j, pickedge in enumerate(['long', 'acute', 'round']):
            axes[1,j].set_title(f'pickedge = {pickedge}')
            for shape in pg.Polygonate(points, pickedge=pickedge, convex=convex).shapes:
                 axes[1,j].plot(*points[[*shape, shape[0]]].T, 'b') # resulting polygons
        fig.tight_layout()
        return fig

.. ipython:: python
    :suppress:

    @savefig convexTrue.png
    plot2(True)

.. ipython:: python
    :suppress:

    @savefig convexFalse.png
    plot2(False)
