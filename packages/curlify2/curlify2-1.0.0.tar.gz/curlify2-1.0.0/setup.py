# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curlify2']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'responses>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'curlify2',
    'version': '1.0.0',
    'description': 'Library to convert python requests and httpx object to curl command.',
    'long_description': 'The library convert python \'requests\' and \'httpx\' object in curl command. Curlify2 is a enhancement of [curlify](\'https://github.com/ofw/curlify\').\n\n\n## Installation\n\nTo install the library use pip or poetry command, see:\n\n```bash\n$ pip install curlify2\n```\n\nor poetry:\n\n```bash\n$ poetry add curlify2\n```\n\n## Usage\n\nusing **requests** module:\n\n```python\nimport curlify2\nimport requests\n\nURL = "https://run.mocky.io/v3/b0f4ffd8-6696-4f90-8bab-4a3bcad9ef3f"\n\nrequest = requests.get(URL)\ncurl = curlify2.to_curl(request.request)\n\nprint(curl) # curl -X GET -H "User-Agent: python-requests/2.24.0" -H "Accept-Encoding: gzip, deflate" -H "Accept: */*" -H "Connection: keep-alive" -d \'None\' https://run.mocky.io/v3/b0f4ffd8-6696-4f90-8bab-4a3bcad9ef3f\n\n```\n\nusing **httpx** module:\n\n```python\nimport curlify2\nimport httpx\n\nURL = "https://run.mocky.io/v3/b0f4ffd8-6696-4f90-8bab-4a3bcad9ef3f"\n\nrequest = httpx.get(URL)\ncurl = curlify2.to_curl(request.request)\n\nprint(curl) # curl -X GET -H "User-Agent: python-requests/2.24.0" -H "Accept-Encoding: gzip, deflate" -H "Accept: */*" -H "Connection: keep-alive" -d \'None\' https://run.mocky.io/v3/b0f4ffd8-6696-4f90-8bab-4a3bcad9ef3f\n\n```',
    'author': 'Marcus Pereira',
    'author_email': 'hi@marcuspereira.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcuxyz/curlify2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
