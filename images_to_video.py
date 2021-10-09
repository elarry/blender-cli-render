"""Script loads rendered images, creates an image sequence, and renders the
image sequence to output a video file.
"""

import bpy
import glob

IMAGE_SEQUENCE_FILEPATH="./output/image_sequence/"

image_list = glob.glob(IMAGE_SEQUENCE_FILEPATH + "*")
bpy.context.scene.frame_end = len(image_list)

seq = bpy.context.scene.sequence_editor.sequences

for frame_num, imagepath in enumerate(image_list):
    seq.new_image(name="img",
                  filepath=imagepath,
                  channel=1,
                  frame_start=frame_num)

bpy.ops.render.render(animation=True)
