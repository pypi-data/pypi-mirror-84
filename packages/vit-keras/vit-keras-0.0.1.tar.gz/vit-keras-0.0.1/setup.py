# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vit_keras']

package_data = \
{'': ['*']}

install_requires = \
['scipy', 'tensorflow-addons', 'validators']

setup_kwargs = {
    'name': 'vit-keras',
    'version': '0.0.1',
    'description': 'Keras implementation of ViT (Vision Transformer)',
    'long_description': "# vit-keras\nThis is a Keras implementation of the models described in [An Image is Worth 16x16 Words:\nTransformes For Image Recognition at Scale](https://arxiv.org/pdf/2010.11929.pdf). It is based on an earlier implementation from [tuvovan](https://github.com/tuvovan/Vision_Transformer_Keras), modified to match the Flax implementation in the [official repository](https://github.com/google-research/vision_transformer).\n\nThe weights here are ported over from the weights provided in the official repository. See `utils.load_weights_numpy` to see how this is done (it's not pretty, but it does the job).\n\n## Usage\nInstall this package using `pip install vit-keras`\n\nYou can use the model out-of-the-box with ImageNet 2012 classes using\nsomething like the following.\n\n```python\nfrom vit_keras import vit, utils\n\nimage_size = 384\nclasses = utils.get_imagenet_classes()\nmodel = vit.vit_b16(\n    image_size=image_size,\n    activation='sigmoid',\n    pretrained=True,\n    include_top=True,\n    pretrained_top=True\n)\nurl = 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Granny_smith_and_cross_section.jpg'\nimage = utils.read(url, image_size)\nX = vit.preprocess_inputs(image).reshape(1, image_size, image_size, 3)\ny = model.predict(X)\nprint(classes[y[0].argmax()]) # Granny smith\n```\n\nYou can fine-tune using a model loaded as follows.\n\n```python\nimage_size = 224\nmodel = vit.vit_l32(\n    image_size=image_size,\n    activation='sigmoid',\n    pretrained=True,\n    include_top=True,\n    pretrained_top=False,\n    classes=200\n)\n# Train this model on your data as desired.\n```\n",
    'author': 'Fausto Morales',
    'author_email': 'faustomorales@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/faustomorales/vit-keras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
