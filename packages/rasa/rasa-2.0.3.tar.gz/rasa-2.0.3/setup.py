# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rasa',
 'rasa.cli',
 'rasa.cli.arguments',
 'rasa.cli.initial_project.actions',
 'rasa.core',
 'rasa.core.actions',
 'rasa.core.brokers',
 'rasa.core.channels',
 'rasa.core.featurizers',
 'rasa.core.nlg',
 'rasa.core.policies',
 'rasa.core.training',
 'rasa.core.training.converters',
 'rasa.nlu',
 'rasa.nlu.classifiers',
 'rasa.nlu.emulators',
 'rasa.nlu.extractors',
 'rasa.nlu.featurizers',
 'rasa.nlu.featurizers.dense_featurizer',
 'rasa.nlu.featurizers.sparse_featurizer',
 'rasa.nlu.selectors',
 'rasa.nlu.tokenizers',
 'rasa.nlu.training_data',
 'rasa.nlu.training_data.converters',
 'rasa.nlu.utils',
 'rasa.nlu.utils.hugging_face',
 'rasa.shared',
 'rasa.shared.core',
 'rasa.shared.core.training_data',
 'rasa.shared.core.training_data.story_reader',
 'rasa.shared.core.training_data.story_writer',
 'rasa.shared.importers',
 'rasa.shared.nlu',
 'rasa.shared.nlu.training_data',
 'rasa.shared.nlu.training_data.formats',
 'rasa.shared.nlu.training_data.schemas',
 'rasa.shared.utils',
 'rasa.utils',
 'rasa.utils.tensorflow']

package_data = \
{'': ['*'],
 'rasa.cli': ['initial_project/*',
              'initial_project/data/*',
              'initial_project/tests/*'],
 'rasa.utils': ['schemas/*']}

install_requires = \
['PyJWT>=1.7,<1.8',
 'SQLAlchemy>=1.3.3,<1.4.0',
 'absl-py>=0.9,<0.11',
 'aiohttp>=3.6,<3.7',
 'apscheduler>=3.6,<3.7',
 'async_generator>=1.10,<1.11',
 'attrs>=19.3,<20.3',
 'boto3>=1.12,<2.0',
 'cloudpickle>=1.2,<1.5',
 'colorclass>=2.2,<2.3',
 'coloredlogs>=10,<15',
 'colorhash>=1.0.2,<1.1.0',
 'fbmessenger>=6.0.0,<6.1.0',
 'joblib>=0.15.1,<0.16.0',
 'jsonpickle>=1.3,<1.5',
 'jsonschema>=3.2,<3.3',
 'kafka-python>=1.4,<3.0',
 'matplotlib>=3.1,<3.4',
 'mattermostwrapper>=2.2,<2.3',
 'multidict>=4.6,<5.0',
 'networkx>=2.4,<2.6',
 'numpy>=1.16,<2.0',
 'oauth2client==4.1.3',
 'packaging>=20.0,<21.0',
 'pika>=1.1.0,<1.2.0',
 'prompt-toolkit>=2.0,<3.0',
 'psycopg2-binary>=2.8.2,<2.9.0',
 'pydot>=1.4,<1.5',
 'pykwalify>=1.7.0,<1.8.0',
 'pymongo[tls,srv]>=3.8,<3.11',
 'python-dateutil>=2.8,<2.9',
 'python-engineio>=3.11,<3.14',
 'python-socketio>=4.4,<4.7',
 'python-telegram-bot>=11.1,<13.0',
 'pytz>=2019.1,<2021.0',
 'questionary>=1.5.1,<1.6.0',
 'rasa-sdk>=2.0.0,<3.0.0',
 'redis>=3.4,<4.0',
 'regex>=2020.6,<2020.10',
 'requests>=2.23,<3.0',
 'rocketchat_API>=0.6.31,<1.10.0',
 'ruamel.yaml>=0.16.5,<0.17.0',
 'sanic-cors>=0.10.0b1,<0.11.0',
 'sanic-jwt>=1.3.2,<1.5.0',
 'sanic>=19.12.2,<21.0.0',
 'scikit-learn>=0.22,<0.24',
 'scipy>=1.4.1,<2.0.0',
 'sentry-sdk>=0.17.0,<0.20.0',
 'setuptools>=41.0.0',
 'sklearn-crfsuite>=0.3,<0.4',
 'slackclient>=2.0.0,<3.0.0',
 'tensorflow-addons>=0.10,<=0.12',
 'tensorflow-estimator>=2.3,<2.4',
 'tensorflow-probability>=0.11,<0.12',
 'tensorflow>=2.3,<2.4',
 'tensorflow_hub>=0.9,<0.10',
 'terminaltables>=3.1.0,<3.2.0',
 'tqdm>=4.31,<4.51',
 'twilio>=6.26,<6.46',
 'ujson>=1.35,<4.0',
 'webexteamssdk>=1.1.1,<1.7.0']

extras_require = \
{':sys_platform != "win32"': ['tensorflow-text>=2.3,<2.4'],
 ':sys_platform == "win32"': ['colorama>=0.4.4,<0.5.0'],
 'full': ['spacy>=2.1,<2.3', 'transformers>=2.4,<2.12', 'jieba>=0.39,<0.43'],
 'gh-release-notes': ['github3.py>=1.3.0,<1.4.0'],
 'jieba': ['jieba>=0.39,<0.43'],
 'spacy': ['spacy>=2.1,<2.3'],
 'transformers': ['transformers>=2.4,<2.12']}

entry_points = \
{'console_scripts': ['rasa = rasa.__main__:main']}

setup_kwargs = {
    'name': 'rasa',
    'version': '2.0.3',
    'description': 'Open source machine learning framework to automate text- and voice-based conversations: NLU, dialogue management, connect to Slack, Facebook, and more - Create chatbots and voice assistants',
    'long_description': '# Rasa Open Source\n\n[![Join the chat on Rasa Community Forum](https://img.shields.io/badge/forum-join%20discussions-brightgreen.svg)](https://forum.rasa.com/?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![PyPI version](https://badge.fury.io/py/rasa.svg)](https://badge.fury.io/py/rasa)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rasa.svg)](https://pypi.python.org/pypi/rasa)\n[![Build Status](https://github.com/RasaHQ/rasa/workflows/Continuous%20Integration/badge.svg)](https://github.com/RasaHQ/rasa/actions)\n[![Coverage Status](https://coveralls.io/repos/github/RasaHQ/rasa/badge.svg?branch=master)](https://coveralls.io/github/RasaHQ/rasa?branch=master)\n[![Documentation Status](https://img.shields.io/badge/docs-stable-brightgreen.svg)](https://rasa.com/docs)\n![Documentation Build](https://img.shields.io/netlify/d2e447e4-5a5e-4dc7-be5d-7c04ae7ff706?label=Documentation%20Build)\n[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B8141%2Fgit%40github.com%3ARasaHQ%2Frasa.git.svg?type=shield)](https://app.fossa.com/projects/custom%2B8141%2Fgit%40github.com%3ARasaHQ%2Frasa.git?ref=badge_shield)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/orgs/RasaHQ/projects/23)\n\n<img align="right" height="244" src="https://www.rasa.com/assets/img/sara/sara-open-source-2.0.png">\n\nRasa is an open source machine learning framework to automate text-and voice-based conversations. With Rasa, you can build contextual assistants on:\n- Facebook Messenger\n- Slack\n- Google Hangouts\n- Webex Teams\n- Microsoft Bot Framework\n- Rocket.Chat\n- Mattermost\n- Telegram\n- Twilio\n- Your own custom conversational channels\n\nor voice assistants as:\n- Alexa Skills\n- Google Home Actions\n\nRasa helps you build contextual assistants capable of having layered conversations with \nlots of back-and-forth. In order for a human to have a meaningful exchange with a contextual \nassistant, the assistant needs to be able to use context to build on things that were previously \ndiscussed – Rasa enables you to build assistants that can do this in a scalable way.\n\nThere\'s a lot more background information in this\n[blog post](https://medium.com/rasa-blog/a-new-approach-to-conversational-software-2e64a5d05f2a).\n\n---\n- **What does Rasa do? 🤔**\n  [Check out our Website](https://rasa.com/)\n\n- **I\'m new to Rasa 😄**\n  [Get Started with Rasa](https://rasa.com/docs/getting-started/)\n\n- **I\'d like to read the detailed docs 🤓**\n  [Read The Docs](https://rasa.com/docs/)\n\n- **I\'m ready to install Rasa 🚀**\n  [Installation](https://rasa.com/docs/rasa/user-guide/installation/)\n\n- **I want to learn how to use Rasa 🚀**\n  [Tutorial](https://rasa.com/docs/rasa/user-guide/rasa-tutorial/)\n\n- **I have a question ❓**\n  [Rasa Community Forum](https://forum.rasa.com/)\n\n- **I would like to contribute 🤗**\n  [How to Contribute](#how-to-contribute)\n\n---  \n## Where to get help\n\nThere is extensive documentation in the [Rasa Docs](https://rasa.com/docs/rasa).\nMake sure to select the correct version so you are looking at\nthe docs for the version you installed.\n\nPlease use [Rasa Community Forum](https://forum.rasa.com) for quick answers to\nquestions.\n\n### README Contents:\n- [How to contribute](#how-to-contribute)\n- [Development Internals](#development-internals)\n- [License](#license)\n\n### How to contribute\nWe are very happy to receive and merge your contributions into this repository! \n\nTo contribute via pull request, follow these steps:\n\n1. Create an issue describing the feature you want to work on (or\n   have a look at the [contributor board](https://github.com/orgs/RasaHQ/projects/23))\n2. Write your code, tests and documentation, and format them with ``black``\n3. Create a pull request describing your changes\n\nFor more detailed instructions on how to contribute code, check out these [code contributor guidelines](CONTRIBUTING.md).\n\nYou can find more information about how to contribute to Rasa (in lots of\ndifferent ways!) [on our website.](http://rasa.com/community/contribute).\n\nYour pull request will be reviewed by a maintainer, who will get\nback to you about any necessary changes or questions. You will\nalso be asked to sign a\n[Contributor License Agreement](https://cla-assistant.io/RasaHQ/rasa).\n\n\n## Development Internals\n\n### Installing Poetry\n\nRasa uses Poetry for packaging and dependency management. If you want to build it from source,\nyou have to install Poetry first. This is how it can be done:\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n```\n\nThere are several other ways to install Poetry. Please, follow \n[the official guide](https://python-poetry.org/docs/#installation) to see all possible options.\n\n### Managing environments\n\nThe official [Poetry guide](https://python-poetry.org/docs/managing-environments/) suggests to use\n[pyenv](https://github.com/pyenv/pyenv) or any other similar tool to easily switch between Python versions. \nThis is how it can be done:\n\n```bash\npyenv install 3.7.6\npyenv local 3.7.6  # Activate Python 3.7.6 for the current project\n```\n\nBy default, Poetry will try to use the currently activated Python version to create the virtual environment \nfor the current project automatically. You can also create and activate a virtual environment manually — in this\ncase, Poetry should pick it up and use it to install the dependencies. For example:\n\n```bash\npython -m venv .venv\nsource .venv/bin/activate\n```\n\nYou can make sure that the environment is picked up by executing \n\n```bash\npoetry env info\n```\n\n### Building from source\n\nTo install dependencies and `rasa` itself in editable mode execute\n\n```bash\nmake install\n```\n\n### Running and changing the documentation\n\nFirst of all, install all the required dependencies:\n\n```bash\nmake install install-docs\n```\n\nAfter the installation has finished, you can run and view the documentation\nlocally using:\n\n```bash\nmake livedocs\n```\n\nIt should open a new tab with the local version of the docs in your browser;\nif not, visit http://localhost:3000 in your browser.\nYou can now change the docs locally and the web page will automatically reload\nand apply your changes.\n\n### Running the Tests\n\nIn order to run the tests, make sure that you have the development requirements installed:\n\n```bash\nmake prepare-tests-ubuntu # Only on Ubuntu and Debian based systems\nmake prepare-tests-macos  # Only on macOS\n```\n\nThen, run the tests:\n\n```bash\nmake test\n```\n\nThey can also be run at multiple jobs to save some time:\n\n```bash\nJOBS=[n] make test\n```\n\nWhere `[n]` is the number of jobs desired. If omitted, `[n]` will be automatically chosen by pytest.\n\n### Resolving merge conflicts\n\nPoetry doesn\'t include any solution that can help to resolve merge conflicts in\nthe lock file `poetry.lock` by default.\nHowever, there is a great tool called [poetry-merge-lock](https://poetry-merge-lock.readthedocs.io/en/latest/).\nHere is how you can install it:\n\n```bash\npip install poetry-merge-lock\n```\n\nJust execute this command to resolve merge conflicts in `poetry.lock` automatically:\n\n```bash\npoetry-merge-lock\n```\n\n### Steps to release a new version\nReleasing a new version is quite simple, as the packages are build and distributed by GitHub Actions.\n\n*Terminology*:\n* patch release (third version part increases): 1.1.2 -> 1.1.3\n* minor release (second version part increases): 1.1.3 -> 1.2.0\n* major release (first version part increases): 1.2.0 -> 2.0.0\n\n*Release steps*:\n1. Make sure all dependencies are up to date (**especially Rasa SDK**)\n    - For Rasa SDK that means first creating a [new Rasa SDK release](https://github.com/RasaHQ/rasa-sdk#steps-to-release-a-new-version) (make sure the version numbers between the new Rasa and Rasa SDK releases match)\n    - Once the tag with the new Rasa SDK release is pushed and the package appears on [pypi](https://pypi.org/project/rasa-sdk/), the dependency in the rasa repository can be resolved (see below).\n2. Switch to the branch you want to cut the release from (`master` in case of a major / minor, the current feature branch for patch releases) \n    - Update the `rasa-sdk` entry in `pyproject.toml` with the new release version and run `poetry update`. This creates a new `poetry.lock` file with all dependencies resolved.\n    - Commit the changes with `git commit -am "bump rasa-sdk dependency"` but do not push them. They will be automatically picked up by the following step.\n3. Run `make release`\n4. Create a PR against master or the release branch (e.g. `1.2.x`)\n5. Once your PR is merged, tag a new release (this SHOULD always happen on master or release branches), e.g. using\n    ```bash\n    git tag 1.2.0 -m "next release"\n    git push origin 1.2.0\n    ```\n    GitHub will build this tag and push a package to [pypi](https://pypi.python.org/pypi/rasa)\n6. **If this is a minor release**, a new release branch should be created pointing to the same commit as the tag to allow for future patch releases, e.g.\n    ```bash\n    git checkout -b 1.2.x\n    git push origin 1.2.x\n    ```\n\n### Code Style\n\nTo ensure a standardized code style we use the formatter [black](https://github.com/ambv/black).\nTo ensure our type annotations are correct we use the type checker [pytype](https://github.com/google/pytype). \nIf your code is not formatted properly or doesn\'t type check, GitHub will fail to build.\n\n#### Formatting\n\nIf you want to automatically format your code on every commit, you can use [pre-commit](https://pre-commit.com/).\nJust install it via `pip install pre-commit` and execute `pre-commit install` in the root folder.\nThis will add a hook to the repository, which reformats files on every commit.\n\nIf you want to set it up manually, install black via `poetry install`.\nTo reformat files execute\n```\nmake formatter\n```\n\n#### Type Checking\n\nIf you want to check types on the codebase, install `pytype` using `poetry install`.\nTo check the types execute\n```\nmake types\n```\n\n### Deploying documentation updates\n\nWe use `Docusaurus v2` to build docs for tagged versions and for the master branch.\nThe static site that gets built is pushed to the `documentation` branch of this repo.\n\nWe host the site on netlify. On master branch builds (see `.github/workflows/documentation.yml`), we push the built docs to\nthe `documentation` branch. Netlify automatically re-deploys the docs pages whenever there is a change to that branch.\n\n\n## License\nLicensed under the Apache License, Version 2.0.\nCopyright 2020 Rasa Technologies GmbH. [Copy of the license](LICENSE.txt).\n\nA list of the Licenses of the dependencies of the project can be found at\nthe bottom of the\n[Libraries Summary](https://libraries.io/github/RasaHQ/rasa).\n',
    'author': 'Rasa Technologies GmbH',
    'author_email': 'hi@rasa.com',
    'maintainer': 'Tom Bocklisch',
    'maintainer_email': 'tom@rasa.com',
    'url': 'https://rasa.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
