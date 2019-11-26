import os
import cv2
import numpy as np
import tifffile as tiff
from matplotlib import pyplot as plt
import tensorflow as tf

dim = (224,224)

def load_data_from_dir(directory):
    data = []
    x = []
    for filename in os.listdir(directory):
        filename = os.fsdecode(filename)
            x.append(os.path.join(directory, filename))

    # read images
    x_images = [cv2.imread(filepath, -1) for filepath in x]
    resized_images = [cv2.resize(image, dim,interpolation = cv2.INTER_AREA) for image in images]
    np_images = np.stack(resized_images, axis=0)
    data.append(np_images)
    return data

def load(images):
    images = load_data_from_dir(path)
    images = np.asarray(images)
    l = images.shape
    images = images.reshape(l[1],l[2],l[3],1)
    return images

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Pass root dir and precessed dir as python pre_processor.py root_dir pre_processed_dir")
        exit(1)
    else:
        x = load(sys.argv[1])
        y = load(sys.argv[2])