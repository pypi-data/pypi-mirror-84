# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lib']

package_data = \
{'': ['*']}

install_requires = \
['WebTest==2.0.35',
 'bottle==0.12.17',
 'loguru==0.5.3',
 'pytest-cov==2.10.1',
 'pytest==5.4.3',
 'requests==2.23.0']

setup_kwargs = {
    'name': 'national-id',
    'version': '1.0.3',
    'description': 'Egyptian national ID validator and data-extractor AP',
    'long_description': '# Egyptian national ID validator and data-extractor API\n\n![[https://pypi.python.org/pypi/national-id](pypi)](https://img.shields.io/pypi/v/national-id.svg)\n[![Actions Status](https://github.com/waleedhammam/national_id/workflows/national_id/badge.svg?query=branch%3Amain)](https://github.com/waleedhammam/national_id/actions?query=branch%3Amain)\n[![codecov.io](https://codecov.io/github/waleedhammam/national_id/coverage.svg?branch=main)](https://codecov.io/github/waleedhammam/national_id?branch=main)\n\n## Requirments\n\n- python3.6 or later\n- pip3\n- bottle\n\n## How to run\n\n- Install requirments `pip3 install -r requirements.txt`\n- Run `python3 server.py`\n- Server will be running on port 8001\n- Endpoint can be reached at http://localhost:8001/get_info\n\n## Endpoint\n\n- `/get_info`\n  - Accepts post requests with "Content-Type: application/json" Header\n    - Example request:\n\n      ```bash\n      curl -H "Content-Type: application/json" -d \'{"id_number": "29009121201812"}\' -XPOST http://localhost:8001/get_info\n      ```\n\n  - Response\n    - 200 OK, json_info: national id is validated and info extraction ok\n    - 400 Bad Request: Wrong national id number\n    - 500 Internal Server Error: Invalid request from user (invalid json, invalid form of data)\n\n    Example response:\n\n      ```bash\n      {"nationl_id_data": {"year_of_birth": "1994", "month_of_birth": "9", "day_of_birth": "15", "governorate": "Al Daqhlia", "type": "Male"}}\n      ```\n\n## Validations and checks\n\n- According to [this source](https://ar.wikipedia.org/wiki/%D8%A8%D8%B7%D8%A7%D9%82%D8%A9_%D8%A7%D9%84%D8%B1%D9%82%D9%85_%D8%A7%D9%84%D9%82%D9%88%D9%85%D9%8A_%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A%D8%A9)\n\nThe national ID consists of the following:\n\n  ```bash\n  +-+--+--+--+--+----+-+\n  |2|90|01|01|12|3456|7|\n  +--------------------+\n  |A|B |C |D |E | F  |G|\n  +-+--+--+--+--+----+-+\n  ```\n\n- A -> The century: A=2 From (1900-1999), A=3 From (2000-2099)\n- B~D (Date of birth):\n    B -> Year of birth\n    C -> Month of birth\n    D -> Day of birth\n- E -> Governorate code ex: {12: "Al Daqhlia"}\n- F -> Unique code. (Odd is male, Even is female)\n- G -> Check digit for verification\n\n## How to run tests\n\n- Lib test: `pytest -s tests/test_national_id.py`\n- Test the endpoint `python3 -m pytest -s tests/test_endpoint.py`\n\n## Dockerfile\n\n- You can build and run the dockerfile in `docker directory`\n  `docker build -t waleedhammam/national_id .`\n\n## Pip installable\n\n- Library national id is pip installable `pip install national-id` to be used in the whole system\n\n- Example usage:\n\n  ```python\n  from lib.national_id import NationalID\n  instance = NationalID("28510291201512")\n  instance.get_info()\n\n  Out:\n  (True,\n   {\'year_of_birth\': \'1985\',\n    \'month_of_birth\': \'10\',\n    \'day_of_birth\': \'29\',\n    \'governorate\': \'Al Daqhlia\',\n    \'type\': \'Male\'})\n  ```\n',
    'author': 'waleedhammam',
    'author_email': 'waleed.hammam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/waleedhammam/national_id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
