# Bounding Box Augmentation

This code is example of augmentating image with bounding boxes.
Augmentable annotation is Pascal VOC only.

## Examples

![original.jpg](docs/original.png)

| Example 1 | Example 2 | Example 3 | Example 4 |
| ---- | ---- | ---- | ---- |
| ![example1.jpg](docs/example1.png) | ![example2.jpg](docs/example2.png) | ![example3.jpg](docs/example3.png) | ![example4.jpg](docs/example4.png) |

## Requirements

 * Python3
 * Pipenv

## Usage

Prepare virtualenv with `pipenv`.

    pipenv install

Put files(Images and Annotations) to augment in `input/`.
(Do not create sub directories.)

Run script.

    pipenv run python augment.py

Augmented images and annotations are generated in `output/`.
