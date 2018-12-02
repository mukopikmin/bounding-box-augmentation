import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import xml.etree.ElementTree as ET
import glob
import shutil

EMPTY_DIR = 'empty'


def parse_xml(filename):
    tree = ET.parse(filename)
    elem = tree.getroot()
    result = {
        'filename': elem.find('.//filename').text,
        'size': {
            'width': elem.find('.//size/width').text,
            'height': elem.find('.//size/height').text,
            'depth': elem.find('.//size/depth').text,
        },
        'objects': []
    }

    for e in elem.findall('.//object'):
        obj = {
            'name': e.find('.//name').text,
            'xmin': e.find('.//bndbox/xmin').text,
            'ymin': e.find('.//bndbox/ymin').text,
            'xmax': e.find('.//bndbox/xmax').text,
            'ymax': e.find('.//bndbox/ymax').text
        }
        result['objects'].append(obj)

    return result


def inspect(filename):
    annotation = parse_xml(filename)

    if len(annotation['objects']) == 0:
        print('Empty annotation file %s is moved.' % filename)
        shutil.move(filename, EMPTY_DIR)
