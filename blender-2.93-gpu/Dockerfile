# Dockerfile adapted from https://github.com/nytimes/rd-blender-docker/blob/master/dist/2.93-gpu-ubuntu18.04/Dockerfile

FROM nvidia/cudagl:10.1-base-ubuntu18.04

# Enviorment variables
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PATH "$PATH:/bin/2.93/python/bin/"
ENV BLENDER_PATH "/bin/2.93"
ENV BLENDERPIP "/bin/2.93/python/bin/pip3"
ENV BLENDERPY "/bin/2.93/python/bin/python3.9"
ENV HW="GPU"

# Install dependencies
RUN apt-get update && apt-get install -y \ 
	wget \ 
	libopenexr-dev \ 
	bzip2 \ 
	build-essential \ 
	zlib1g-dev \ 
	libxmu-dev \ 
	libxi-dev \ 
	libxxf86vm-dev \ 
	libfontconfig1 \ 
	libxrender1 \ 
	libgl1-mesa-glx \ 
	xz-utils

# Download and install Blender
RUN wget https://mirror.clarkson.edu/blender/release/Blender2.93/blender-2.93.0-linux-x64.tar.xz \ 
	&& tar -xvf blender-2.93.0-linux-x64.tar.xz --strip-components=1 -C /bin \ 
	&& rm -rf blender-2.93.0-linux-x64.tar.xz \ 
	&& rm -rf blender-2.93.0-linux-x64 

# Download the Python source since it is not bundled with Blender
RUN wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz \ 
	&& tar -xzf Python-3.9.1.tgz \ 
	&& cp -r Python-3.9.1/Include/* $BLENDER_PATH/python/include/ \ 
	&& rm -rf Python-3.9.1.tgz \ 
	&& rm -rf Python-3.9.1 

# Blender comes with a super outdated version of numpy (which is needed for matplotlib / opencv) so override it with a modern one
RUN rm -rf ${BLENDER_PATH}/python/lib/site-packages/numpy 

# Must first ensurepip to install Blender pip3 and then new numpy
RUN ${BLENDERPY} -m ensurepip && ${BLENDERPIP} install --upgrade pip && ${BLENDERPIP} install numpy

RUN mkdir /app
RUN mkdir /app/output

COPY ./*.py app/

# Set the working directory
WORKDIR /app
