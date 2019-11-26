"""Pre Processor by @KdPisda
    Author: Kuldeep Pisda
    Git: [at]kdpisda
    Email: kdpisda[at]gmail.com
Job:
    It pre process the kaggle dataset given here https://www.kaggle.com/c/ultrasound-nerve-segmentation
"""

import os
import shutil
import getopt, sys
import Augmentor

def load_data_from_dir(root_dir, processed_dir):

    print("Main Dir: {}".format(root_dir))
    print("Processed Image Dir: {}".format(processed_dir))
    directory = root_dir
    """
    Trying to create a train directory under procecssed_dir
    """
    if not os.path.exists(os.path.join(processed_dir, "train")):
        try:
            os.makedirs(os.path.join(processed_dir, "train"))
        except OSError as e:
            print(e)
            raise
    
    """
    Trying to create a train directory under procecssed_dir
    """
    if not os.path.exists(os.path.join(processed_dir, "train_mask")):
        try:
            os.makedirs(os.path.join(processed_dir, "train_mask"))
        except OSError as e:
            print(e)
            raise

    train_dir = os.path.join(processed_dir, "train")
    train_mask_dir = os.path.join(processed_dir, "train_mask")

    y = []
    for filename in os.listdir(directory):
        filename = os.fsdecode(filename)
        print("Filename: {}".format(os.path.join(train_mask_dir, filename)))
        if filename.endswith("mask.tif"):
            new_filename = filename.replace("_mask.tif", ".tif")
            print("New Filename: {}".format(os.path.join(root_dir, new_filename)))
            shutil.copy(os.path.join(root_dir, filename), os.path.join(train_mask_dir, new_filename))
        else:
            shutil.copy(os.path.join(root_dir, filename), os.path.join(train_dir, filename))

def augment(image_path, mask_path):
    p = Augmentor.Pipeline(image_path)
    p.ground_truth(mask_path)
    p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
    p.flip_left_right(probability=0.5)
    p.zoom_random(probability=0.5, percentage_area=0.8)
    p.flip_top_bottom(probability=0.5)
    p.sample(10000)

if __name__ == "__main__":
    # full_cmd_args = sys.args
    # arguments_list = full_cmd_args[1:]
    # unixOptions = "ho:v"
    # gnuOptions = ["main-dir", "processed-dir"]
    # try:
    #     arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    # except getopt.error as err:
    #     # output error, and return with an error code
    #     print (str(err))
    #     sys.exit(2)
    # for currentArgument, currentValue in arguments:
    #     if currentArgument in ("--main-dir"):
    #         print ("main-dir")
    #     elif currentArgument in ("-h", "--help"):
    #         print ("displaying help")
    #     elif currentArgument in ("-o", "--output"):
    #         print (("enabling special output mode (%s)") % (currentValue))
    if len(sys.argv) < 3:
        print("Pass root dir and precessed dir as python pre_processor.py root_dir pre_processed_dir")
        exit(1)
    else:
        if os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]):
            load_data_from_dir(sys.argv[1], sys.argv[2])
        else:
            if not os.path.exists(sys.argv[2]):
                try:
                    os.makedirs(sys.argv[2])
                    load_data_from_dir(sys.argv[1], sys.argv[2])
                except OSError as e:
                    print(e)
                    raise
        image_path = os.path.join(sys.argv[2], "train")
        image_mask_path = os.path.join(sys.argv[2], "train_mask")
        augment(image_path, image_mask_path)
