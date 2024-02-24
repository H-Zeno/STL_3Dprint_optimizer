import numpy as np
from STL_edit import STL_model, rotX, rotY, rotZ


# Load the STL model
STL_file = STL_model('humanoid.stl')

# Read the STL file
STL_file.read_stl_text()

# Make manipulations on the loaded STL file
#STL_file.scale(0.5)
#STL_file.translate([0,0,5])
STL_file.rotate(rotY(0.5*np.pi))

# Save the new STL file
STL_file.write_stl_text('humanoid_rotated_90Y.stl')