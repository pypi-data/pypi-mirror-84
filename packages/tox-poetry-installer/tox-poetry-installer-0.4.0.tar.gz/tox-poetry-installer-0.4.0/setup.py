# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tox_poetry_installer', 'test_metadata']
install_requires = \
['poetry-core>=1.0.0,<2.0.0', 'poetry>=1.0.0,<2.0.0', 'tox>=2.3.0,<4.0.0']

entry_points = \
{'tox': ['poetry_installer = tox_poetry_installer']}

setup_kwargs = {
    'name': 'tox-poetry-installer',
    'version': '0.4.0',
    'description': 'Tox plugin to install Tox environment dependencies using the Poetry backend and lockfile',
    'long_description': "# tox-poetry-installer\n\nA plugin for [Tox](https://tox.readthedocs.io/en/latest/) that allows test environment\ndependencies to be installed using [Poetry](https://python-poetry.org/) from its lockfile.\n\n⚠️ **This project is alpha software and should not be used in production environments** ⚠️\n\n[![ci-status](https://github.com/enpaul/tox-poetry-installer/workflows/CI/badge.svg?event=push)](https://github.com/enpaul/tox-poetry-installer/actions)\n[![license](https://img.shields.io/pypi/l/tox-poetry-installer)](https://opensource.org/licenses/MIT)\n[![pypi-version](https://img.shields.io/pypi/v/tox-poetry-installer)](https://pypi.org/project/tox-poetry-installer/)\n[![python-versions](https://img.shields.io/pypi/pyversions/tox-poetry-installer)](https://www.python.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Documentation**\n\n* [Installation](#installation)\n* [Quick Start](#quick-start)\n* [Usage Examples](#usage-examples)\n* [Known Drawbacks and Problems](#known-drawbacks-and-problems)\n* [Why would I use this?](#why-would-i-use-this) (What problems does this solve?)\n* [Developing](#developing)\n* [Contributing](#contributing)\n* [Roadmap](#roadmap)\n  * [Path to Beta](#path-to-beta)\n  * [Path to Stable](#path-to-stable)\n\nRelated resources:\n* [Poetry Python Project Manager](https://python-poetry.org/)\n* [Tox Automation Project](https://tox.readthedocs.io/en/latest/)\n* [Poetry Dev-Dependencies Tox Plugin](https://github.com/sinoroc/tox-poetry-dev-dependencies)\n* [Poetry Tox Plugin](https://github.com/tkukushkin/tox-poetry)\n* [Other Tox plugins](https://tox.readthedocs.io/en/latest/plugins.html)\n\n\n## Installation\n\nAdd the plugin as a development dependency of a Poetry project:\n\n```\n~ $: poetry add tox-poetry-installer --dev\n```\n\nConfirm that the plugin is installed, and Tox recognizes it, by checking the Tox version:\n\n```\n~ $: poetry run tox --version\n3.20.0 imported from .venv/lib64/python3.8/site-packages/tox/__init__.py\nregistered plugins:\n    tox-poetry-installer-0.2.2 at .venv/lib64/python3.8/site-packages/tox_poetry_installer.py\n```\n\nIf using Pip, ensure that the plugin is installed to the same environment as Tox:\n\n```\n# Calling the virtualenv's 'pip' binary directly will cause pip to install to that virtualenv\n~ $: /path/to/my/automation/virtualenv/bin/pip install tox\n~ $: /path/to/my/automation/virtualenv/bin/pip install tox-poetry-installer\n```\n\n\n## Quick Start\n\nTo require a Tox environment install all it's dependencies from the Poetry lockfile, add the\n`require_locked_deps = true` option to the environment configuration and remove all version\nspecifiers from the dependency list. The versions to install will be taken from the lockfile\ndirectly:\n\n```ini\n[testenv]\ndescription = Run the tests\nrequire_locked_deps = true\ndeps =\n    pytest\n    pytest-cov\n    black\n    pylint\n    mypy\ncommands = ...\n```\n\nTo require specific dependencies be installed from the Poetry lockfile, and let the rest be\ninstalled using the default Tox installation backend, add the suffix `@poetry` to the dependencies.\nIn the example below the `pytest`, `pytest-cov`, and `black` dependencies will be installed from\nthe lockfile while `pylint` and `mypy` will be installed using the versions specified here:\n\n```ini\n[testenv]\ndescription = Run the tests\nrequire_locked_deps = true\ndeps =\n    pytest@poetry\n    pytest-cov@poetry\n    black@poetry\n    pylint >=2.5.0\n    mypy == 0.770\ncommands = ...\n```\n\nAlternatively, to quickly install all Poetry dev-dependencies to a Tox environment, add the\n`install_dev_deps =  true` option to the environment configuration. This option can be used either\nwith the `require_locked_deps = true` option or without it\n\n**Note:** Regardless of the settings outlined above, all dependencies of the project package (the\none Tox is testing) will always be installed from the lockfile.\n\n\n## Usage Examples\n\nAfter installing the plugin to a project your Tox automation is already benefiting from the\nlockfile: when Tox installs your project package to one of your environments, all the dependencies\nof your project package will be installed using the versions specified in the lockfile. This\nhappens automatically and requires no configuration changes.\n\nBut what about the rest of your Tox environment dependencies?\n\nLet's use an example `tox.ini` file, below, that defines two environments: the main `testenv` for\nrunning the project tests and `testenv:check` for running some other helpful tools:\n\n```ini\n[tox]\nenvlist = py37, static\nisolated_build = true\n\n[testenv]\ndescription = Run the tests\ndeps =\n    pytest == 5.3.0\ncommands = ...\n\n[testenv:check]\ndescription = Static formatting and quality enforcement\ndeps =\n    pylint >=2.4.4,<2.6.0\n    mypy == 0.770\n    black --pre\ncommands = ...\n```\n\nLet's focus on the `testenv:check` environment first. In this project there's no reason that any\nof these tools should be a different version than what a human developer is using when installing\nfrom the lockfile. We can require that these dependencies be installed from the lockfile by adding\nthe option `require_locked_deps = true` to the environment config, but this will cause an error:\n\n```ini\n[testenv:check]\ndescription = Static formatting and quality enforcement\nrequire_locked_deps = true\ndeps =\n    pylint >=2.4.4,<2.6.0\n    mypy == 0.770\n    black --pre\ncommands = ...\n```\n\nRunning Tox using this config gives us this error:\n\n```\ntox_poetry_installer.LockedDepVersionConflictError: Locked dependency 'pylint >=2.4.4,<2.6.0' cannot include version specifier\n```\n\nThis is because we told the Tox environment to require all dependencies be locked, but then also\nspecified a specific version constraint for Pylint. With the `require_locked_deps = true` setting\nTox expects all dependencies to take their version from the lockfile, so when it gets conflicting\ninformation it errors. We can fix this by simply removing all version specifiers from the\nenvironment dependency list:\n\n```ini\n[testenv:check]\ndescription = Static formatting and quality enforcement\nrequire_locked_deps = true\ndeps =\n    pylint\n    mypy\n    black\ncommands = ...\n```\n\nNow all the dependencies will be installed from the lockfile. If Poetry updates the lockfile with\na new version then that updated version will be automatically installed when the Tox environment is\nrecreated.\n\nNow let's look at the `testenv` environment. Let's make the same changes to the `testenv`\nenvironment that we made to `testenv:check` above; remove the PyTest version and add\n`require_locked_deps = true`. Then imagine that we want to add the\n[Requests](https://requests.readthedocs.io/en/master/) library to the test environment: we\ncan add `requests` as a dependency of the test environment, but this will cause an error:\n\n```ini\n[testenv]\ndescription = Run the tests\nrequire_locked_deps = true\ndeps =\n    pytest\n    requests\ncommands = ...\n```\n\nRunning Tox with this config gives us this error:\n\n```\ntox_poetry_installer.LockedDepNotFoundError: No version of locked dependency 'requests' found in the project lockfile\n```\n\nThis is because `requests` is not in our lockfile yet. Tox will refuse to install a dependency\nthat isn't in the lockfile to an an environment that specifies `require_locked_deps = true`. We\ncan fix this by running `poetry add requests --dev` to add it to the lockfile.\n\nNow let's combine dependencies from the lockfile with dependencies that are\nspecified in-line in the Tox environment configuration.\n[This isn't generally recommended](#why-would-i-use-this), but it is a valid use case and\nfully supported by this plugin. Let's modify the `testenv` configuration to install PyTest\nfrom the lockfile but then install an older version of the Requests library.\n\nThe first thing to do is remove the `require_locked_deps = true` setting so that we can install\nRequests as an unlocked dependency. Then we can add our version specifier to the `requests`\nentry in the dependency list:\n\n```ini\n[testenv]\ndescription = Run the tests\ndeps =\n    pytest\n    requests >=2.2.0,<2.10.0\ncommands = ...\n```\n\nHowever we still want `pytest` to be installed from the lockfile, so the final step is to tell Tox\nto install it from the lockfile by adding the suffix `@poetry` to the `pytest` entry in the\ndependency list:\n\n```ini\n[testenv]\ndescription = Run the tests\ndeps =\n    pytest@poetry\n    requests >=2.2.0,<2.10.0\ncommands = ...\n```\n\nNow when the `testenv` environment is created it will install PyTest (and all of its dependencies)\nfrom the lockfile while it will install Requests (and all of its dependencies) using the default\nTox installation backend.\n\n\n## Known Drawbacks and Problems\n\n* The following `tox.ini` configuration options have no effect on the dependencies installed from\n  the Poetry lockfile (note that they will still affect unlocked dependencies):\n  * [`install_command`](https://tox.readthedocs.io/en/latest/config.html#conf-install_command)\n  * [`pip_pre`](https://tox.readthedocs.io/en/latest/config.html#conf-pip_pre)\n  * [`downloadcache`](https://tox.readthedocs.io/en/latest/config.html#conf-downloadcache) (deprecated)\n  * [`download`](https://tox.readthedocs.io/en/latest/config.html#conf-download)\n  * [`indexserver`](https://tox.readthedocs.io/en/latest/config.html#conf-indexserver)\n  * [`usedevelop`](https://tox.readthedocs.io/en/latest/config.html#conf-indexserver)\n\n* Tox environments automatically inherit their settings from the main `testenv` environment. This\n  means that if the `require_locked_deps = true` is specified for the `testenv` environment then\n  all environments will also require locked dependencies. This can be overwritten by explicitly\n  specifying `require_locked_deps = false` on child environments where unlocked dependencies are\n  needed.\n\n* There are a handful of packages that cannot be installed from the lockfile, whether as specific\n  dependencies or as transient dependencies (dependencies of dependencies). This is due to\n  [an ongoing discussion in the Poetry project](https://github.com/python-poetry/poetry/issues/1584);\n  the list of dependencies that cannot be installed from the lockfile can be found\n  [here](https://github.com/python-poetry/poetry/blob/cc8f59a31567f806be868aba880ae0642d49b74e/poetry/puzzle/provider.py#L55).\n  This plugin will skip these dependencies entirely, but log a warning when they are encountered.\n\n\n## Why would I use this?\n\n**Introduction**\n\nThe lockfile is a file generated by a package manager for a project that records what\ndependencies are installed, the versions of those dependencies, and any additional metadata that\nthe package manager needs to recreate the local project environment. This allows developers\nto have confidence that a bug they are encountering that may be caused by one of their\ndependencies will be reproducible on another device. In addition, installing a project\nenvironment from a lockfile gives confidence that automated systems running tests or performing\nbuilds are using the same environment as a developer.\n\n[Poetry](https://python-poetry.org/) is a project dependency manager for Python projects, and\nso it creates and manages a lockfile so that its users can benefit from all the features\ndescribed above. [Tox](https://tox.readthedocs.io/en/latest/#what-is-tox) is an automation tool\nthat allows Python developers to run tests suites, perform builds, and automate tasks within\nself-contained [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).\nTo make these environments useful Tox supports installing dependencies in each environment.\nHowever, since these environments are created on the fly and Tox does not maintain a lockfile,\nthere can be subtle differences between the dependencies a developer is using and the\ndependencies Tox uses.\n\nThis is where this plugin comes into play.\n\nBy default Tox uses [Pip](https://docs.python.org/3/tutorial/venv.html) to install the\nPEP-508 compliant dependencies to a test environment. This plugin extends the default\nTox dependency installation behavior to support installing dependencies using a Poetry-based\ninstallation method that makes use of the dependency metadata from Poetry's lockfile.\n\n**The Problem**\n\nEnvironment dependencies for a Tox environment are usually specified in PEP-508 format, like\nthe below example:\n\n```ini\n# from tox.ini\n...\n\n[testenv]\ndescription = Some very cool tests\ndeps =\n    foo == 1.2.3\n    bar >=1.3,<2.0\n    baz\n\n...\n```\n\nLet's assume these dependencies are also useful during development, so they can be added to the\nPoetry environment using this command:\n\n ```\n poetry add --dev \\\n    foo==1.2.3 \\\n    bar>=1.3,<2.0 \\\n    baz\n ```\n\n However there is a potential problem that could arise from each of these environment\n dependencies that would _only_ appear in the Tox environment and not in the Poetry\n environment in use by a developer:\n\n * **The `foo` dependency is pinned to a specific version:** let's imagine a security\n   vulnerability is discovered in `foo` and the maintainers release version `1.2.4` to fix\n   it. A developer can run `poetry remove foo` and then `poetry add foo^1.2` to get the new\n   version, but the Tox environment is left unchanged. The development environment, as defined by\n   the lockfile, is now patched against the vulnerability but the Tox environment is not.\n\n* **The `bar` dependency specifies a dynamic range:** a dynamic range allows a range of\n  versions to be installed, but the lockfile will have an exact version specified so that\n  the Poetry environment is reproducible; this allows versions to be updated with\n  `poetry update` rather than with the `remove` and `add` commands used above. If the\n  maintainers of `bar` release version `1.6.0` then the Tox environment will install it\n  because it is valid for the specified version range. Meanwhile the Poetry environment will\n  continue to install the version from the lockfile until `poetry update bar` explicitly\n  updates it. The development environment is now has a different version of `bar` than the Tox\n  environment.\n\n* **The `baz` dependency is unpinned:** unpinned dependencies are\n  [generally a bad idea](https://python-poetry.org/docs/faq/#why-are-unbound-version-constraints-a-bad-idea),\n  but here it can cause real problems. Poetry will interpret an unbound dependency using\n  [the carrot requirement](https://python-poetry.org/docs/dependency-specification/#caret-requirements)\n  but Pip (via Tox) will interpret it as a wildcard. If the latest version of `baz` is `1.0.0`\n  then `poetry add baz` will result in a constraint of `baz>=1.0.0,<2.0.0` while the Tox\n  environment will have a constraint of `baz==*`. The Tox environment can now install an\n  incompatible version of `baz` and any errors that causes cannot be replicated using `poetry update`.\n\nAll of these problems can apply not only to the dependencies specified for a Tox environment,\nbut also to the dependencies of those dependencies, those dependencies' dependencies, and so on.\n\n**The Solution**\n\nThis plugin allows dependencies specified in Tox environment take their version directly from\nthe Poetry lockfile without needing an independent version to be specified in the Tox\nenvironment configuration. The modified version of the example environment given below appears\nless stable than the one presented above because it does not specify any versions for its\ndependencies:\n\n```ini\n# from tox.ini\n...\n\n[testenv]\ndescription = Some very cool tests\nrequire_locked_deps = true\ndeps =\n    foo\n    bar\n    baz\n\n...\n```\n\nHowever with the `tox-poetry-installer` plugin installed the `require_locked_deps = true`\nsetting means that Tox will install these dependencies from the Poetry lockfile so that the\nversion installed to the Tox environment exactly matches the version Poetry is managing. When\n`poetry update` updates the lockfile with new versions of these dependencies, Tox will\nautomatically install these new versions without needing any changes to the configuration.\n\n\n## Developing\n\nThis project requires a developer to have Poetry version 1.0+ installed on their workstation, see\nthe [installation instructions here](https://python-poetry.org/docs/#installation).\n\n```bash\n# Clone the repository...\n# ...over HTTPS\ngit clone https://github.com/enpaul/tox-poetry-installer.git\n# ...over SSH\ngit clone git@github.com:enpaul/tox-poetry-installer.git\n\n# Create a the local project virtual environment and install dependencies\ncd tox-poetry-installer\npoetry install\n\n# Install pre-commit hooks\npoetry run pre-commit install\n\n# Run tests and static analysis\npoetry run tox\n```\n\n\n## Contributing\n\nAll project contributors and participants are expected to adhere to the\n[Contributor Covenant Code of Conduct, Version 2](CODE_OF_CONDUCT.md).\n\nThe `devel` branch has the latest (potentially unstable) changes. The\n[tagged versions](https://github.com/enpaul/tox-poetry-installer/releases) correspond to the\nreleases on PyPI.\n\n* To report a bug, request a feature, or ask for assistance, please\n  [open an issue on the Github repository](https://github.com/enpaul/tox-poetry-installer/issues/new).\n* To report a security concern or code of conduct violation, please contact the project author\n  directly at **ethan dot paul at enp dot one**.\n* To submit an update, please\n  [fork the repository](https://docs.github.com/en/enterprise/2.20/user/github/getting-started-with-github/fork-a-repo)\n  and\n  [open a pull request](https://github.com/enpaul/tox-poetry-installer/compare).\n\n\n## Roadmap\n\nThis project is under active development and is classified as alpha software, not yet ready\nfor usage in production environments.\n\n* Beta classification will be assigned when the initial feature set is finalized\n* Stable classification will be assigned when the test suite covers an acceptable number of\n  use cases\n\n### Path to Beta\n\n- [X] Verify that primary package dependencies (from the `.package` env) are installed\n      correctly using the Poetry backend.\n- [X] Support the [`extras`](https://tox.readthedocs.io/en/latest/config.html#conf-extras)\n      Tox configuration option ([#4](https://github.com/enpaul/tox-poetry-installer/issues/4))\n- [X] Add per-environment Tox configuration option to fall back to default installation\n      backend.\n- [ ] Add warnings when an unsupported Tox configuration option is detected while using the\n      Poetry backend. ([#5](https://github.com/enpaul/tox-poetry-installer/issues/5))\n- [X] Add trivial tests to ensure the project metadata is consistent between the pyproject.toml\n      and the module constants.\n- [X] Update to use [poetry-core](https://github.com/python-poetry/poetry-core) and\n      improve robustness of the Tox and Poetry module imports\n      to avoid potentially breaking API changes in upstream packages. ([#2](https://github.com/enpaul/tox-poetry-installer/issues/2))\n- [ ] Find and implement a way to mitigate the [UNSAFE_DEPENDENCIES issue](https://github.com/python-poetry/poetry/issues/1584) in Poetry.\n      ([#6](https://github.com/enpaul/tox-poetry-installer/issues/6))\n- [ ] Fix logging to make proper use of Tox's logging reporter infrastructure ([#3](https://github.com/enpaul/tox-poetry-installer/issues/3))\n- [ ] Add configuration option for installing all dev-dependencies to a testenv ([#14](https://github.com/enpaul/tox-poetry-installer/issues/14))\n\n### Path to Stable\n\nEverything in Beta plus...\n\n- [ ] Add tests for each feature version of Tox between 2.3 and 3.20\n- [ ] Add tests for Python-3.6, 3.7, and 3.8\n- [X] Add Github Actions based CI\n- [ ] Add CI for CPython, PyPy, and Conda\n- [ ] Add CI for Linux and Windows\n",
    'author': 'Ethan Paul',
    'author_email': '24588726+enpaul@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enpaul/tox-poetry-installer/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
