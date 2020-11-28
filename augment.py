import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import cv2
from pascal_voc_writer import Writer
import xml.etree.ElementTree as ET
import glob
from util import sequence
from util import annotation as an
import shutil
import sys

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
AUGMENT_SIZE = 10


def main():
    for file in glob.glob('%s/*.xml' % INPUT_DIR):
        print('Augmenting %s ...' % file)
        annotation = an.parse_xml(file)
        augment(annotation)

    for file in glob.glob('%s/*.xml' % OUTPUT_DIR):
        an.inspect(file)


def augment(annotation):
    seq = sequence.get()

    for i in range(AUGMENT_SIZE):
        filename = annotation['filename']
        sp = filename.split('.')
        outfile = '%s/%s-%02d.%s' % (OUTPUT_DIR, sp[0], i, sp[-1])

        seq_det = seq.to_deterministic()

        image = cv2.imread('%s/%s' % (INPUT_DIR, annotation['filename']))
        _bbs = []
        for obj in annotation['objects']:
            bb = ia.BoundingBox(x1=int(obj['xmin']),
                                y1=int(obj['ymin']),
                                x2=int(obj['xmax']),
                                y2=int(obj['ymax']),
                                label=obj['name'])
            _bbs.append(bb)

        bbs = ia.BoundingBoxesOnImage(_bbs, shape=image.shape)

        image_aug = seq_det.augment_images([image])[0]
        bbs_aug = seq_det.augment_bounding_boxes(
            [bbs])[0].remove_out_of_image().cut_out_of_image()

        writer = Writer(outfile,
                        annotation['size']['width'],
                        annotation['size']['height'])
        for bb in bbs_aug.bounding_boxes:
            if int((bb.x2-bb.x1)*(bb.y2-bb.y1)) == 0:
                print("augmentet boundingbox has non existing area. Skipping")
                continue
            writer.addObject(bb.label,
                             int(bb.x1),
                             int(bb.y1),
                             int(bb.x2),
                             int(bb.y2))

        cv2.imwrite(outfile, image_aug)
        writer.save('%s.xml' % outfile.split('.')[0])


if __name__ == '__main__':
    main()
