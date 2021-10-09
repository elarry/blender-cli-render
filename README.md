Programmatic Blender Render
===========================

This project shows how to use python scripts to automate the manual steps of creating an animation. For example, we can create parameterized scripts that control aspects of the animation that enable you to generate multiple variants of renders quickly circumventing the normal manual workflow using blender's GUI.

**Script Output**:

[![Blender animation](https://img.youtube.com/vi/orCrpGGHD2o/0.jpg)](https://youtu.be/orCrpGGHD2o)


**Credit**:

- Both the animation and the Python code was inspired by [Olav3D Tutorials](https://www.youtube.com/watch?v=KI0tjZUkb5A)
- Dockerfiles are from: https://github.com/nytimes/rd-blender-docker


## Rendering Animation from the Command-line


**STEP 1:** Create `.blend` file from python script:
```shell
mkdir -p output
blender -b -P blender_cubes.py -- output/blender_cubes.blend
```
Note that the last argument above is passed in to the Python script where it specifies the output file name (yes, it's important to include whitespace around the double-dash).

**STEP 2:** Create image sequence by rendering`.blend` file.
 while passing in 
```shell
blender -b output/blender_cubes.blend -E CYCLES -s 1 -e 250 -o output/image_sequence/img_ -F PNG -P gpu_settings.py -a
```
The render settings can be passed in separate python scripts:

- For GPU rendering pass `gpu_settings.py`.  
- For CPU rendering, replace `-P gpu_settings.py -a` with `-a -- --cycles-device CPU`
    + Whitespace and order of `-a` argument important
- Without any script, Blender will use the default render settings.

**STEP 3:** Create animation from image sequence:
```shell
blender -b -F AVIJPEG -o output/blender_cubes.avi -P images_to_video.py
```

### Command-line Arguments

- `-b` : Background. Render in background.
- `-P` : Python
- `-a` : Animation. Render theanimation using the settings saved in the blend-file.
- `-E` : Render engine. Run `blender -E help` to see all engines available. e.g. `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`.
- `-f 10` : Render only the 10th frame.
- `-f -2` : Render only the second last frame.
- `-F MY_RENDER_FORMAT` : Valid render format options include: `PNG`, `BMP`, `AVIJPEG`, `AVIRAW`,`FFMPEG`, `TGA`, `RAWTGA`, `JPEG`, `IRIS`, `IRIZ`.

For more common Blender CLI arguments, see official documentation at:
https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html

## Run in Docker Container

Navigate to project root
```shell
docker build -t "$USER/blender-2.93-gpu" -f ./blender-2.93-gpu/Dockerfile .
docker run --gpus all -v `pwd`/output:/app/output -it $USER/blender-2.93-gpu bash
```

From within Docker container:
```shell
blender -b -P blender_cubes.py -- output/blender_cubes.blend
blender -b output/blender_cubes.blend -E CYCLES -s 0 -e 250 -o output/image_sequence/img_ -F PNG -P gpu_settings.py -a
blender -b -F FFMPEG -o output/blender_cubes.mpg -P images_to_video.py
```


## General Beginner Tips for Creating Python Scripts from Blender

- Open three Blender sub-windows:
    + 3D Viewport
    + Scripting -> Text Editor: Script editor: writing code
    + Scrpting -> Info
- From main menu bar Window -> Toggle System Console
    + This opens a seprate screen where you see python errors
- Workflow:
    + Create object in viewport as you would normally.
    + See corresponding python code appear in info screen
    + Copy paste code from info screen to text editor
    + When executing "Run Script", debug by looking at blender system console error messages
- Gotchas:
    + Include delete commands at the beginning of python script. Otherwise objects might get multiplied with each run of the script.


## Links to Other Related Projects

- https://github.com/yuki-koyama/blender-cli-rendering
- https://github.com/Vogete/blender-cuda-docker
