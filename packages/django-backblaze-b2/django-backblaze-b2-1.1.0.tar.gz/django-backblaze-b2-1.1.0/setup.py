# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_backblaze_b2']

package_data = \
{'': ['*']}

install_requires = \
['b2sdk>=1.1.4,<2.0.0', 'django>=3.0']

setup_kwargs = {
    'name': 'django-backblaze-b2',
    'version': '1.1.0',
    'description': 'A Django app to use backblaze b2 as storage.',
    'long_description': '# django-backblaze-b2\n\n[![pypi version](https://img.shields.io/pypi/v/django-backblaze-b2)](https://pypi.org/project/django-backblaze-b2/)\n[![python version](https://img.shields.io/pypi/pyversions/django-backblaze-b2)](https://pypi.org/project/django-backblaze-b2/)\n[![django version](https://img.shields.io/pypi/djversions/django-backblaze-b2)](https://pypi.org/project/django-backblaze-b2/)\n\nA storage backend for Django that uses [Backblaze\'s B2 APIs](https://www.backblaze.com/b2/cloud-storage.html).\n\nImplementation wraps [Official Python SDK](https://github.com/Backblaze/b2-sdk-python)\n\n## How to use\n\n1. Install from this repo, or install from PyPi: `pip install django-backblaze-b2`\nAs tested, requires python 3.6 or greater but solely due to type annotations. PRs welcome :)\n1. Configure your django `settings`. The absolute minimum config would be:\n```python\nBACKBLAZE_CONFIG = {\n    "application_key_id": os.getenv("BACKBLAZE_KEY_ID"), # however you want to securely retrieve these values\n    "application_key": os.getenv("BACKBLAZE_KEY"),\n}\n```\n\nTheoretically you may now refer to the base storage class as a storage class.  \ne.g.\n```python\nfrom django_backblaze_b2 import BackblazeB2Storage\n\nclass MyModel(models.Model):\n    fileField = models.FileField(\n        upload_to="uploads",\n        storage=BackblazeB2Storage\n    )\n```\n\n### Public/Logged-In/Private storage\n\n1. Add `django_backblaze_b2` to your `INSTALLED_APPS`\n1. Add the urls to your `urlpatterns` in the root `urls.py`:\n```python\n    urlpatterns = [\n        ...\n        path(\'\', include(\'django_backblaze_b2.urls\')),\n    ]\n```\n\n### Configurations \n\nYou may want to use your own bucket name, or set further configuration such as lazy authorization/validation, or specifying file metadata.  \nRefer to [the options](./django_backblaze_b2/options.py) for all options.  \nYou can modify the settings dict, but additionally override any setting with the `opts` keyword argument to the storage classes.\n\nTo specify different buckets to use for your public, logged-in, staff storage, you can set the \n`specificBucketNames` attribute of the settings dict.\n\n## Why\n\nThere are several Django storage packages out there already which support B2, but none met my needs. These are:\n\n* [django-storages](https://github.com/jschneier/django-storages)\n    * Large community engagement ✅\n    * Well-tested ✅\n    * [Second-class support](https://github.com/jschneier/django-storages/issues/765) via [Apache Libcloud](https://github.com/apache/libcloud) ❌\n    * Disconnect in configuration and actual use ❌\n    * PR list with low turnaround ❌\n* [django-b2](https://github.com/pyutil/django-b2)\n    * Similar aim to this project, around official backblaze SDK ✅\n    * Mixed goals (storage, scripts) ❌\n    * Tests?? ❌\n* [django-backblazeb2-storage](https://github.com/royendgel/django-backblazeb2-storage)\n    * Simple configuration ✅\n    * Not based around python SDK (potentially harder to keep up with version changes) ❌\n    * Tests?? ❌\n\n### S3 Compatible API\n\nBackblazed can be used with an [S3-compatible API](https://www.backblaze.com/b2/docs/s3_compatible_api.html)\nThis is great, but most packages use an older version of the S3 Api (v2). Backblaze uses v4.\n\n### What this package offers\n\n* Type Annotations\n* Tested\n* No hacks required to get up and running around API deficiencies (any hacks are not exposed in API)\n* Support for public/private files, restricted via Django user permissions\n\n## How it works\n\n* A simple implementation of the `django.core.files.storage.Storage` class provides handling for storage behaviour within your Django application\n* Three url routes are appended to the root of your application:  \n    1. `/b2/`\n    2. `/b2l/`\n    3. `/b2s/`\nThese routes act as a proxy/intermediary between the requester and backblaze b2 apis. The public `/b2/` allows exposing files from a private bucket, and the logged-in and staff routes will perform the known validations of a django app to prevent unauthorized access.\n\n### Gotchas\n\n* The original filename + any upload paths is stored in the database. Thus your column name must be of sufficient length to hold that (unchanged behaviour from `FileSystemStorage`)\n*  When retrieving files from the `PublicStorage`, `LoggedInStorage` or `StaffStorage`, you may not override the `"bucket"` or authorization options, or else when the app proxies the file download, it will be unable to retrieve the file from the respective bucket.\n* Simply using `LoggedInStorage` or `StaffStorage` is not enough to protect your files if your bucket is not public. If any individual gains access to the file ids/urls for these files, there is no authentication around them. It is up to the implementer to ensure the security of their application.\n* Once the file is uploaded, and someone obtains a file url (e.g. http://djangodomain.com/b2l/uploads/image.png), the model will no longer be checked for the file. This means that if you share the bucket between multiple use-cases, you could in theory find finds that don\'t belong to your django app, or similarly if you delete/change your models, the files could still be downloaded. Consider using an app like [django-cleanup](https://github.com/un1t/django-cleanup) if this is important to you\n\n## Contributing\n\nContributions welcome!\n\n* Please ensure test coverage does not decrease in a meaningful way.\n* Ensure formatting is compliant (`make lint`)\n* Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)\n\n## Setting up for development\n\n### Requires\n\n* python\n* GNU Make\n* (optional) pyenv - align local version\n* (optional) docker - run sample app\n\n### Running\n\n1. `make setup`\n\n* You can run django with `make run-django` to test django app.\n* You can run tests with `make test`\n* You can view test coverage with `make test-coverage`, then see in the terminal, \nopen `test/htmlcov/index.html`\nor use `cov.xml` in your favourite IDE like VSCode\n\n### Releasing\n\n1. `TWINE_PASSWORD=<api key> make release`\n\n### Cleanup\n\n1. `make cleanup`\n',
    'author': 'Étienne H',
    'author_email': 'django_backblaze_b2@internet-e-mail.com',
    'maintainer': 'Étienne H',
    'maintainer_email': 'django_backblaze_b2@internet-e-mail.com',
    'url': 'https://github.com/ehossack/django-backblaze-b2/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
