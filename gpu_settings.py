"""This script adapted from https://blender.stackexchange.com/a/156680
"""

import bpy


def enable_gpus(device_type, use_cpus=False, tile_size=()):
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cuda_devices, opencl_devices = cycles_preferences.get_devices()

    if device_type == "CUDA":
        devices = cuda_devices
    elif device_type == "OPENCL":
        devices = opencl_devices
    else:
        raise RuntimeError("Unsupported device type")

    activated_gpus = []

    for device in devices:
        if device.type == "CPU":
            device.use = use_cpus
        else:
            device.use = True
            activated_gpus.append(device.name)

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"
    
    if len(tile_size) > 0:
        bpy.context.scene.render.tile_x = tile_size[0]
        bpy.context.scene.render.tile_y = tile_size[1]

    return activated_gpus


enable_gpus("CUDA", tile_size=(512, 512))
