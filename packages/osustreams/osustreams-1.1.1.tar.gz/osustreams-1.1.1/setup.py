# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['is_it_stream']
entry_points = \
{'console_scripts': ['osustreams = is_it_stream:main']}

setup_kwargs = {
    'name': 'osustreams',
    'version': '1.1.1',
    'description': 'find stream maps in your osu library',
    'long_description': '# OSU-STREAM-DETECTOR\n- An osu tool for finding stream maps in your map library\n- Try online : https://osufiles.github.io/stream-map/ \n\n# Install \n- python - Python 3.6+\n- download is_it_stream.py or `pip install osustreams`\n\n# Usage\nAs a single is_it_stream.py file\n- run from console , `python is_it_stream.py`  with optional arguments\n- check output file with name `Stream maps[{min_bpm}-{max_bpm}] {timestamp}.txt`\n\nAs a pip package \n```\nusage: osustreams [-h] [--collection] [-a A] [-b B]\noptional arguments:\n  -h, --help        show this help message and exit\n  --collection, -c  export to in-game collection\n  -a A              Min bpm\n  -b B              Max bpm\n  --ignore, -i      ignore bad unicode\n```\n- example :`osustreams -a 110 -b 170 -c` \n- this will create in-game collection with beatmaps where a = min BPM , b = max BPM\n\nstream_detector.ini - should be located in Lib/site-packages (if you wish to edit path to osu/songs) \nNote: As of current, this tool can only scan maps from around 2016-present due to differences in file formatting\n\n# This is a fork\nhttps://github.com/iMeisa/OSMF\n',
    'author': 'upgradeq',
    'author_email': 'noreply@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upgradeQ/OSU-STREAM-DETECTOR',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
