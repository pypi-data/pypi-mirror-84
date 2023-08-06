# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydub-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydub-stubs',
    'version': '0.24.1.5',
    'description': 'Stub-only package containing type information for pydub',
    'long_description': "# pydub-stubs\n\nPydub version: **0.24.1**\n\n**`pydub-stubs` provides type information for Pydub.**<br>\nOnly the public interface is guaranteed to be typed.\n\n```\npip install pydub-stubs\n```\n\n<br>\n\n## Aniticipated Questions\n\n### Q: Why is <code>AudioSegment.<i>some_effect(...)</i></code> missing?\n\n**TL;DR:** Import it as a function from `pydub.effects`.\n\nPydub dynamically adds certain functions to `AudioSegment` at runtime.\nThis is easy to type, but impossible to be 100% safe about.\n\nA great example of why this can is difficult is `pydub.scipy_effects`,\nwhich registers two effects that are named identically to those in\n`pydub.effects`, but have different signatures. Importing this module\nwill override the previous effects, so now the signatures are wrong.\n\n### Q: What the hell is that version number?\n\n`major.minor.patch.stubs`, where major/minor/patch are the latest\nsupported Pydub version. The stubs version being last means pinning\nto a specific Pydub version will always get the latest stubs available.\n\n<br>\n\n## Changelog\n\n### Version 0.24.1.5\n\n* **Fix `AudioSegment.export`**\n  First param is named `out_f` and isn't required.\n\n<details>\n<summary>Previous versions</summary>\n\n### Version 0.24.1.4\n\n* **Improved signature of `AudioSegment.from_file`**<br>\n  The keyword arguments for raw/PCM audio don't require `format` to be\n  set to either `raw` or `pcm`.\n\n* **Fix package exports**<br>\n  Exports `AudioSegment` from `__init__.py`.\n\n### Version 0.24.1.3\n\n* **Fixed overloads of `AudioSegment.fade`**<br>\n  Exactly two of `start`, `end`, and `duration` must be given.\n\n### Version 0.24.1.2\n\n* **Improved `AudioSegment.fade`**<br>\n  Changed to use overloads to prevent invalid method calls.\n\n* **Improved `AudioSegment.from_mono_audiosegments`**<br>\n  Use a positional-only parameter to ensure there's at least 1 argument.\n\n### Version 0.24.1.1\n\n* **Fixed `AudioSegment.__init__`**<br>\n  Use overloads to model correct parameters.\n\n* **Fixed `AudioSegment._spawn`**<br>\n  Parameter `overrides` accepts a partial dictionary.\n\n* **Fixed `pydub.scipy_effects.high_pass_filter`**<br>\n  Parameter `order` should be `int`, not `float`.\n\n### Version 0.24.1.0\n\nReleased\n\n</details>\n",
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SeparateRecords/pydub-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
