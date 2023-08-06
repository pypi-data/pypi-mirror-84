# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gest', 'gest.annotation', 'gest.annotation.gesture', 'gest.examples']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'onnxruntime>=1.4.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0', 'pynput']

setup_kwargs = {
    'name': 'gest',
    'version': '0.3.0',
    'description': 'Hand gestures as an input device',
    'long_description': '# gest\nHand gestures as an input device\n\n![example](https://raw.githubusercontent.com/bm371613/gest/master/images/example.gif)\n\n## Why\nFor health related reasons, I had to stop using a mouse and a keyboard. [Talon](https://talonvoice.com/) allowed me to type with my voice and move the cursor with my eyes. This project was started to complement this setup with hand gestures.\n\n## Development status\nThe project is in an early stage of development. I use it on daily basis, so it should be good enough for some.\n\nWhat is implemented:\n- pinching gesture recognition, in one hand orientation\n- heatmap output, separate for left and right hand, indicating pinched point position\n- demo for testing recognition models\n- example script for simulating mouse clicks and scrolling\n- scripts for producing and reviewing training data\n\n### Bias\nThe gesture recognition model was trained on images of my hands, taken with my hardware in my working environment, so it is probably heavily biased.\nI hope people who want to use it, but recognition quality prevents them from it, would capture some images of their hands using included tooling and donate it to the project, so that over time it works well for everyone.\n\n## Installation\n\nUse Python 3.6, 3.7 or 3.8 and [in a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) run\n\n`pip install gest`\n\nIf you clone this repository, you can get the exact versions of required libraries that I am using with [Poetry](https://python-poetry.org/)\n\n`poetry install`\n\n## Walkthrough\n\n### Demo\n\nFirst check how the included model works for you. Run\n\n`python -m gest.demo`\n\nand see if it recognizes your gestures as here:\n\n![demo](https://raw.githubusercontent.com/bm371613/gest/master/images/demo.gif)\n\nIf you have multiple cameras, you can pick one like\n\n`python -m gest.demo --camera 2`\n\nCamera numbers are not necessarily consecutive.\nTwo cameras may be accessible as 0 and 2.\nThis option is supported by other commands as well.\n\n### Example script\n\nIn the presentation on top I am running\n\n`python -m gest.examples.two_handed_scroll_and_click`\n\nIt only acts if it detects both hands pinching and based on their relative position:\n- double clicks if you cross your hands\n- scrolls up or down if your hands pinch at different heights\n- left clicks if your hands (almost) touch\n- right clicks if your hands are on the same height, but not close horizontally (this action is delayed by a fraction of a second to prevent accidental use)\n\n### Controlling CPU load\n\nFor everyday use, you don\'t want to dedicate too much resources to gesture recognition. You can control it by setting `OMP_NUM_THREADS`, as in\n\n`OMP_NUM_THREADS=2 python -m gest.examples.two_handed_scroll_and_click`\n\nTry different values to find balance between responsiveness and CPU load.\n\n## Custom scripts\n\nThe demo and example scripts serve two additional purposes:\nthey can be used as templates for custom scripts\nand they define the public API for the purpose of semantic versioning.\n\n## Training data annotation\n\n### Capturing\n\n`python -m gest.annotation.capture --countdown 5 data_directory`\n\nwill help you create annotated images.\nOnce you start automatic annotation (press `a` to start/stop) it will ask you to pinch a given point with your left or right hand, or to not pinch ("background").\n\nYou will have 5 seconds before the image is captured (the `--countdown`).\n\nYou will also see the last annotated image for quick review. It can be deleted with `d`.\n\n### Reviewing\n\n`python -m gest.annotation.review --time 1 data_directory closed_pinch_left`\n\nwill let you review all images annotated as left hand pinch in `data_directory`, showing you each for 1 second if you start/stop automatic advancing with `a`. Otherwise you can go to the next/previous image with `n`/`p`. Delete incorrectly annotated images with `d`.\n\nYou should also review `closed_pinch_right` and `background`.\n\n### Annotation guidelines\nIt makes sense to annotate realistic training data that the model performs poorly on, like if\n- it mistakenly detects a pinch when you pick up the phone,\n- it doesn\'t detect pinching when you wear a skin colored shirt.\n\nIf it performs poorly overall, it\'s good to capture the images in many short sessions, with different lighting, clothes, background, camera angle.\n\nThe point isn\'t though to look for tricky cases or stretch the definition of a pinching gesture to include a different hand orientation (eg. with pinching fingers pointing towards the camera).\n\n### Donating annotated data\nContact me [b.marcinkowski@leomail.pl](mailto:b.marcinkowski@leomail.pl)\n',
    'author': 'Bartosz Marcinkowski',
    'author_email': 'b.marcinkowski@leomail.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bm371613/gest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
