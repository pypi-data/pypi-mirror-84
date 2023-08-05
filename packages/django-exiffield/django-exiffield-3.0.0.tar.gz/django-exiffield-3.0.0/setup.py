# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exiffield']

package_data = \
{'': ['*']}

install_requires = \
['choicesenum>=0.2.2', 'django>=2.2', 'jsonfield>=3.0', 'pillow>=5.0']

setup_kwargs = {
    'name': 'django-exiffield',
    'version': '3.0.0',
    'description': 'django-exiffield extracts exif information by utilizing the exiftool.',
    'long_description': "# django-exiffield\n\n![PyPI](https://img.shields.io/pypi/v/django-exiffield?style=flat-square)\n![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/escaped/django-exiffield/Test%20&%20Lint/master?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/django-exiffield/master?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-exiffield?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/django-exiffield?style=flat-square)\n\ndjango-exiffield extracts exif information by utilizing the exiftool.\n\n## Requirements\n\n* Python 3.6.1 or newer\n* [exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/)\n* Django >= 2.2\n\n## Installation\n\n1. Install django-exiffield\n\n   ```sh\n   pip install django-exiffield\n   ```\n\n2. Make sure `exiftool` is executable from you environment.\n\n## Integration\n\nLet's assume we have an image Model with a single `ImageField`.\nTo extract exif information for an attached image, add an `ExifField`,\nspecify the name of the `ImageField` in the `source` argument\n\n```python\nfrom django.db import models\n\nfrom exiffield.fields import ExifField\n\n\nclass Image(models.Model):\n    image = models.ImageField()\n    exif = ExifField(\n        source='image',\n    )\n```\n\nand create a migration for the new field.\nThat's it.\n\nAfter attaching an image to your `ImageField`, the exif information is stored\nas a `dict` on the `ExifField`.\nEach exif information of the dictionary consists of two keys:\n\n* `desc`: A human readable description\n* `val`: The value for the entry.\n\nIn the following example we access the camera model\n\n```python\nimage = Image.objects.get(...)\nprint(image.exif['Model'])\n# {\n#     'desc': 'Camera Model Name',\n#     'val': 'DMC-GX7',\n# }\n```\n\nAs the exif information is encoded in a simple `dict` you can iterate and access\nthe values with all familiar dictionary methods.\n\n## Denormalizing Fields\n\nSince the `ExifField` stores its data simply as text, it is not possible to filter\nor access indiviual values efficiently.\nThe `ExifField` provides a convinient way to denormalize certain values using\nthe `denormalized_fields` argument.\nIt takes a dictionary with the target field as key and a simple getter function of\ntype `Callable[[Dict[Dict[str, str]]], Any]`.\nTo denormalize a simple value you can use the provided `exiffield.getters.exifgetter`\n\n```python\nfrom django.db import models\n\nfrom exiffield.fields import ExifField\nfrom exiffield.getters import exifgetter\n\n\nclass Image(models.Model):\n    image = models.ImageField()\n    camera = models.CharField(\n        editable=False,\n        max_length=100,\n    )\n    exif = ExifField(\n        source='image',\n        denormalized_fields={\n            'camera': exifgetter('Model'),\n        },\n    )\n```\n\nThere are more predefined getters in `exiffield.getters`:\n\n`exifgetter(exif_key: str) -> str`  \nGet an unmodified exif value.\n\n`get_type() -> str`  \nGet file type, e.g. video or image\n\n`get_datetaken -> Optional[datetime]`  \nGet when the file was created as `datetime`\n\n`get_orientation  -> exiffield.getters.Orientation`  \nGet orientation of media file.\nPossible values are `LANDSCAPE` and `PORTRAIT`.\n\n`get_sequenctype -> exiffield.getters.Mode`  \nGuess if the image was taken in a sequence.\nPossible values are `BURST`, `BRACKETING`, `TIMELAPSE` and `SINGLE`.\n\n`get_sequencenumber -> int`  \nGet image position in a sequence.\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual enviroment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n\n### Cookiecutter template\n\nThis project was created using [cruft](https://github.com/cruft/cruft) and the\n[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.\nIn order to update this repository to the latest template version run\n\n```sh\ncruft update\n```\n\nin the root of this repository.\n\n",
    'author': 'Alexander Frenzel',
    'author_email': 'alex@relatedworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/escaped/django-exiffield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
