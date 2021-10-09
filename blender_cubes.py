"""Script creates a .blend file with a baked animation that can be executed 
from the command line.

Note that the bpy module is not a standalone Python module, but is only 
available from Blender's built in Python interpreter. Though there is a workaround
https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule
"""

import bpy
import sys


# Clear all
bpy.ops.ptcache.free_bake_all()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set world Background to black
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

# Create plane
bpy.ops.mesh.primitive_plane_add(size=100, enter_editmode=False, location=(0, 0, -40))

## Add physics to plane
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'
bpy.context.object.rigid_body.collision_shape = 'MESH'
bpy.context.object.rigid_body.collision_margin = 0

# Add Sun
bpy.ops.object.light_add(type='SUN', radius=2, location=(0, 0, 0), rotation=(0, 1, 5))
bpy.context.object.data.energy = 2

# Add Camera
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(40, -9.18, -19), rotation=(1.14494, 1.01332e-07, 1.17286))
bpy.context.object.data.lens = 30  # Focal Length in mm
bpy.context.scene.camera = bpy.context.object  # Needed for command line render

# Create Material using Material Nodes
material = bpy.data.materials.new(name="Diffuse")
material.use_nodes = True
material_output = material.node_tree.nodes.get('Material Output')
diffuse = material.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
diffuse.inputs['Color'].default_value = (0.27, 0.18, 0.8, 1) # RGB + alpha
material.node_tree.links.new(material_output.inputs[0], diffuse.outputs[0])

# Create Cubes
n_x = 4 # Number of replications in x-direction
n_y = 4  # Number of replications in y-direction
n_z = 4  # Number of replications in z-direction
step_size = 2
epsilon = 0.005
obj_size = step_size - epsilon  # Create small buffer between objects

x_count = 0
for x in range(0, n_x):
    x_count += step_size
    y_count = 0
    for y in range(0, n_y):
        y_count += step_size
        z_count = 0
        for z in range(0, n_z):
            bpy.ops.mesh.primitive_cube_add(size=obj_size, location=(x_count, y_count, z_count))
            z_count += step_size

            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.mass = 20
            bpy.context.object.rigid_body.collision_shape = 'BOX'
            bpy.context.object.rigid_body.friction = 1
            bpy.context.object.rigid_body.restitution = 0.2  # Bounciness
            bpy.context.object.rigid_body.use_margin = True
            bpy.context.object.rigid_body.collision_margin = 0
            bpy.context.object.rigid_body.linear_damping = 0.35
            bpy.context.object.rigid_body.angular_damping = 0.6

            # Set Material
            bpy.context.object.active_material = material

# Bake all physics as a final step so that dynamics will be animated
bpy.ops.ptcache.bake_all(bake=True)

if __name__ == "__main__":
    OUTPUT_BLEND_FILE = sys.argv[-1]
    print(OUTPUT_BLEND_FILE)
    bpy.ops.wm.save_mainfile(filepath=OUTPUT_BLEND_FILE)  # Create .blend file
