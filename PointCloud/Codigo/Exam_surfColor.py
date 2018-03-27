###############################################################
# Create some data
import numpy as np
x, y = np.mgrid[0:10:100j, 0:10:100j]
z = x**2 + y**2
w = np.arctan(x/y)

###############################################################
# Visualize the data
from enthought.mayavi import mlab

# Create the data source
src = mlab.pipeline.array2d_source(z)

# Add the additional scalar information 'w', this is where we need to be a bit careful,
# see
# http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/auto/example_atomic_orbital.html
# and
# http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/data.html
dataset = src.mlab_source.dataset
array_id = dataset.point_data.add_array(w.T.ravel())
dataset.point_data.get_array(array_id).name = 'color'
dataset.point_data.update()

# Here, we build the very exact pipeline of surf, but add a
# set_active_attribute filter to switch the color, this is code very
# similar to the code introduced in:
# http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/mlab.html#assembling-pipelines-with-mlab
warp = mlab.pipeline.warp_scalar(src, warp_scale=.5)
normals = mlab.pipeline.poly_data_normals(warp)
active_attr = mlab.pipeline.set_active_attribute(normals,
                                            point_scalars='color')
surf = mlab.pipeline.surface(active_attr)

# Finally, add a few decorations.
mlab.axes()
mlab.outline()
mlab.view(-177, 82)
mlab.show()