import sys
from os import path

sys.path.append(path.abspath(path.dirname(__file__)))

import tqdm
import random
import pathlib
import itertools
import collections
import os
import cv2
import numpy as np
import remotezip as rz
import tensorflow as tf

# Some modules to display an animation using imageio.
import imageio.v2 as imageio
from IPython import display
from urllib import request
# from tensorflow_docs.vis import embed


def list_files_from_zip_url(zip_url):
    """List the files in each class of the dataset given a URL with the zip file.

    Args:
        zip_url: A URL from which the files can be extracted from.

    Returns:
        List of files in each of the classes.
    """
    files = []
    with rz.RemoteZip(zip_url) as zip:
        for zip_info in zip.infolist():
            files.append(zip_info.filename)
    return files


def get_class(fname):
    """Retrieve the name of the class given a filename.

    Args:
        fname: Name of the file in the UCF101 dataset.

    Returns:
        Class that the file belongs to.
    """
    return fname.split("_")[-3]


def get_files_per_class(files):
    """Retrieve the files that belong to each class.

    Args:
        files: List of files in the dataset.

    Returns:
        Dictionary of class names (key) and files (values).
    """
    files_for_class = collections.defaultdict(list)
    for fname in files:
        class_name = get_class(fname)
        files_for_class[class_name].append(fname)
    return files_for_class


def select_subset_of_classes(files_for_class, classes, files_per_class):
    """Create a dictionary with the class name and a subset of the files in that class.

    Args:
        files_for_class: Dictionary of class names (key) and files (values).
        classes: List of classes.
        files_per_class: Number of files per class of interest.

    Returns:
        Dictionary with class as key and list of specified number of video files in that class.
    """
    files_subset = dict()

    for class_name in classes:
        class_files = files_for_class[class_name]
        files_subset[class_name] = class_files[:files_per_class]

    return files_subset


def download_from_zip(zip_url, to_dir, file_names):
    """Download the contents of the zip file from the zip URL.

    Args:
        zip_url: A URL with a zip file containing data.
        to_dir: A directory to download data to.
        file_names: Names of files to download.
    """
    with rz.RemoteZip(zip_url) as zip:
        for fn in tqdm.tqdm(file_names):
            class_name = get_class(fn)
            zip.extract(fn, str(to_dir / class_name))
            unzipped_file = to_dir / class_name / fn

            fn = pathlib.Path(fn).parts[-1]
            output_file = to_dir / class_name / fn
            unzipped_file.rename(output_file)


def split_class_lists(files_for_class, count):
    """Returns the list of files belonging to a subset of data as well as the remainder of
    files that need to be downloaded.

    Args:
        files_for_class: Files belonging to a particular class of data.
        count: Number of files to download.

    Returns:
        Files belonging to the subset of data and dictionary of the remainder of files that need to be downloaded.
    """
    split_files = []
    remainder = {}
    for cls in files_for_class:
        split_files.extend(files_for_class[cls][:count])
    remainder[cls] = files_for_class[cls][count:]
    return split_files, remainder


def download_ucf_101_subset(zip_url, num_classes, splits, download_dir):
    """Download a subset of the UCF101 dataset and split them into various parts, such as
    training, validation, and test.

    Args:
        zip_url: A URL with a ZIP file with the data.
        num_classes: Number of labels.
        splits: Dictionary specifying the training, validation, test, etc. (key) division of data
                (value is number of files per split).
        download_dir: Directory to download data to.

    Return:
        Mapping of the directories containing the subsections of data.
    """
    files = list_files_from_zip_url(zip_url)
    for f in files:
        path = os.path.normpath(f)
        tokens = path.split(os.sep)
        if len(tokens) <= 2:
            # Remove that item from the list if it does not have a filename
            files.remove(f)

    files_for_class = get_files_per_class(files)

    classes = list(files_for_class.keys())[:num_classes]

    for cls in classes:
        random.shuffle(files_for_class[cls])

    # Only use the number of classes you want in the dictionary
    files_for_class = {x: files_for_class[x] for x in classes}

    dirs = {}
    for split_name, split_count in splits.items():
        print(split_name, ":")
    split_dir = download_dir / split_name
    split_files, files_for_class = split_class_lists(files_for_class, split_count)
    download_from_zip(zip_url, split_dir, split_files)
    dirs[split_name] = split_dir

    return dirs


def format_frames(frame, output_size):
    """
    Pad and resize an image from a video.

    Args:
        frame: Image that needs to resized and padded.
        output_size: Pixel size of the output frame image.

    Return:
        Formatted frame with padding of specified output size.
    """
    frame = tf.image.convert_image_dtype(frame, tf.float32)
    frame = tf.image.resize_with_pad(frame, *output_size)
    return frame


def frames_from_video_file(video_path, n_frames, output_size=(224, 224), frame_step=15):
    """
    Creates frames from each video file present for each category.

    Args:
        video_path: File path to the video.
        n_frames: Number of frames to be created per video file.
        output_size: Pixel size of the output frame image.

    Return:
        An NumPy array of frames in the shape of (n_frames, height, width, channels).
    """
    # Read each video frame by frame
    result = []
    src = cv2.VideoCapture(str(video_path))

    video_length = src.get(cv2.CAP_PROP_FRAME_COUNT)

    need_length = 1 + (n_frames - 1) * frame_step

    if need_length > video_length:
        start = 0
    else:
        max_start = video_length - need_length
        start = random.randint(0, max_start + 1)

    src.set(cv2.CAP_PROP_POS_FRAMES, start)
    # ret is a boolean indicating whether read was successful, frame is the image itself
    ret, frame = src.read()
    result.append(format_frames(frame, output_size))

    for _ in range(n_frames - 1):
        for _ in range(frame_step):
            ret, frame = src.read()
        if ret:
            frame = format_frames(frame, output_size)
            result.append(frame)
        else:
            result.append(np.zeros_like(result[0]))
    src.release()
    result = np.array(result)[..., [2, 1, 0]]

    return result


def to_gif(images):
    converted_images = np.clip(images, 0, 255).astype(np.uint8)
    imageio.mimsave("./animation.gif", converted_images, fps=25)
    # return embed.embed_file("./animation.gif")
