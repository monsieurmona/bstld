#!/usr/bin/env python
"""
Crop traffic light images to the format 720 * 960 and save them into a separate folder

Example usage:
    python resize_tl_images input.yaml output_folder
"""
import sys
import os
import cv2
from read_label_file import get_all_labels
from show_label_images import ir
import yaml

def resize_tl_images(input_yaml, output_folder, height, width):
    """
    Fetches all labelled pictures of traffic lights
    Resizes them
    Stores them into a seperate folder
    Adapts the yaml file
    :param input_yaml: Path to yaml file
    :param output_folder: path to folder. created if does not exist
    """
    images = get_all_labels(input_yaml)

    assert output_folder is not None

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    yaml_base_filename = os.path.basename(input_yaml)
    image_subfolder = os.path.splitext(yaml_base_filename)[0]
    image_output_folder = os.path.join(output_folder, image_subfolder)

    if not os.path.exists(image_output_folder):
        os.makedirs(image_output_folder)

    new_yaml = []

    j = 1
    for i, image_dict in enumerate(images):
        image = cv2.imread(image_dict['path'])

        if image is None:
            print 'Could not open image path', image_dict['path']
            continue

        orig_height, orig_width, _ = image.shape

        margin_top = int((orig_height - height) / 2)
        margin_left = int((orig_width - width) / 2)
        
        new_filename = str(j).zfill(6) + '.png'

        new_boxes = []

        for box in image_dict['boxes']:
            xmin = ir(box['x_min'])
            ymin = ir(box['y_min'])
            xmax = ir(box['x_max'])
            ymax = ir(box['y_max'])
            if xmax-xmin<=0 or ymax-ymin<=0:
                continue

            if xmin < margin_left or xmax < margin_left:
                continue

            if xmin > margin_left + width or xmax > margin_left + width:
                continue

            if ymin < margin_top or ymax < margin_top:
                continue

            if ymin > margin_top + height or ymax > margin_top + height:
                continue

            box['x_min'] = xmin - margin_left
            box['y_min'] = ymin - margin_top
            box['x_max'] = xmax - margin_left
            box['y_max'] = ymax - margin_top

            new_boxes.append(box)

        if (len(new_boxes) > 0):
            image_dict['boxes'] = new_boxes
            image_dict['path'] = os.path.join(".", image_subfolder, new_filename)
            new_yaml.append(image_dict)

            image_crop = image[margin_top:margin_top + height, margin_left:margin_left + width]
            cropped_image_filename = os.path.join(image_output_folder, new_filename)

            cv2.imwrite(cropped_image_filename, image_crop)
            # cv2.imshow('Image', image_crop)
            # cv2.waitKey(0)

        j += 1

    yaml_output_filename = os.path.join(output_folder, yaml_base_filename)

    with open(yaml_output_filename, 'w') as yaml_output_file:
        yaml.dump(new_yaml, yaml_output_file, default_flow_style=True)

    #yaml.dump(new_yaml, )


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(-1)
    label_file = sys.argv[1]
    output_folder = sys.argv[2]
    resize_tl_images(label_file, output_folder=output_folder, height=720, width=960)