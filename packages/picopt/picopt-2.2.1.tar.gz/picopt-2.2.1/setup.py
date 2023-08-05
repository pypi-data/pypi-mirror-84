# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picopt', 'picopt.formats', 'tests', 'tests.integration', 'tests.unit']

package_data = \
{'': ['*'],
 'tests': ['test_files/comic_archives/*',
           'test_files/images/*',
           'test_files/invalid/*']}

install_requires = \
['Pillow>=6,<9', 'python-dateutil>=2.8,<3.0', 'rarfile>=4.0,<5.0']

entry_points = \
{'console_scripts': ['picopt = picopt.cli:main']}

setup_kwargs = {
    'name': 'picopt',
    'version': '2.2.1',
    'description': 'A multi format lossless image optimizer that uses external tools',
    'long_description': "# picopt\n\nA multi-format, recursive, multiprocessor aware, command line lossless image optimizer utility that uses external tools to do the optimizing.\n\nPicopt depends on Python [PIL](http://www.pythonware.com/products/pil/) to identify files and Python [rarfile](https://pypi.python.org/pypi/rarfile) to open CBRs.\n\nThe actual image optimization is accomplished by external programs.\n\nTo optimize JPEG images. Picopt needs one of [mozjpeg](https://github.com/mozilla/mozjpeg) or [jpegtran](http://jpegclub.org/jpegtran/) on the path. in order of preference.\n\nTo optimize lossless images like PNG, PNM, GIF, and BMP, picopt requires either [optipng](http://optipng.sourceforge.net/) or [pngout](http://advsys.net/ken/utils.htm) be on the path. Optipng provides the most advantage, but best results are acheived by using pngout as well.\n\nAnimated GIFs are optimized with [gifsicle](http://www.lcdf.org/gifsicle/) if it is available. Picopt nag you to convert your file to [HTML5 video](http://gfycat.com/about), but does not provide this service itself.\n\nPicopt uncompresses, optimizes and rezips [comic book archive files](https://en.wikipedia.org/wiki/Comic_book_archive). Be aware that CBR rar archives will be rezipped into CBZs instead of CBR. Comic book archive optimization is not turned on by default to prevent surprises.\n\nPicopt allows you to drop picopt timestamps at the root of your recursive optimization trees so you don't have to remember which files to optimize or when you last optimized them.\n\n## Installation\n\n### Lossless external program packages\n\n#### macOS\n\n    brew install optipng mozjpeg gifsicle\n    ln -s /usr/local/Cellar/mozjpeg/3.1/bin/jpegtran /usr/local/bin/mozjpeg\n    brew install jonof/kenutils/pngout\n\n#### Debian / Ubuntu\n\n    apt-get install optipng gifsicle python-imaging\n\nif you don't want to install mozjpeg using the instructions below then use jpegtran:\n\n    apt-get install libjpeg-progs\n\n#### Redhat / Fedora\n\n    yum install optipng gifsicle python-imaging\n\nif you don't want to install mozjpeg using the instructions below then use jpegtran:\n\n    yum install libjpeg-progs\n\n#### MozJPEG\n\nmozjpeg offers better compression than libjpeg-progs' jpegtran. As of Jan 2020 it may or\nmay not be packaged for your \\*nix, but even when it is, picopt requires\nthat its separately compiled version of jpegtran be symlinked to 'mozjpeg'\nsomewhere in the path. This installation example is for OS X:\n\n    ln -s /usr/local/Cellar/mozjpeg/3.3/bin/jpegtran /usr/local/bin/mozjpeg\n\nYou may find Linux instructions on [Andrew Welch's blog](https://nystudio107.com/blog/installing-mozjpeg-on-ubuntu-16-04-forge)\n\n#### pngout\n\npngout is a useful compression to use after optipng. It is not packaged for linux, but you may find the latest binary version [on JonoF's site](http://www.jonof.id.au/kenutils). Picopt looks for the binary to be called `pngout`\n\n### Picopt python package\n\n    pip install picopt\n\n## Usage\n\nOptimize all JPEG files in a dirctory:\n\n    picopt *.jpg\n\nOptimize all files and recurse directories:\n\n    picopt -r *\n\nOptimize files and recurse directories AND optimize comic book archives:\n\n    picopt -rc *\n\nOptimize files, but not lossless files:\n\n    picopt -OPG *\n\nOptimize files, but not jpegs:\n\n    picopt -JT *\n\nOptimize files, but not animated gifs:\n\n    picopt -G *\n\nJust list files picopt.py would try to optimize:\n\n    picopt -l *\n\nOptimize everything in my iPhoto library, but only after the last time i did this, skipping symlinks to avoid massive amounts of duplicate work. Don't convert lossless files to PNGs because that would confuse iPhoto. Also drop a timestamp file so I don't have to remember the last time I did this:\n\n    picopt -rSYt -D '2013 June 1 14:00' 'Pictures/iPhoto Library'\n\n## Gotchas\n\nPicopt automatically uses timestamp files if it detects them in or above the current directory tree. A situation can arise with comic archives where the comic archive itself is newer than the timestamp file so it is processed, but the files inside the archive are older than the timestamp file so they are not. Currently the workaround is to move the comic archive outside of the current tree into a temporary directory and process it there.\n\n## Packaged For\n\n- [PyPI](https://pypi.python.org/pypi/picopt/)\n- [Arch Linux](https://aur.archlinux.org/packages/picopt/)\n\n## Alternatives\n\n[imagemin](https://github.com/imagemin/imagemin-cli) looks to be an all in one cli and gui solution with bundled libraries, so no awkward dependancies.\n[Imageoptim](http://imageoptim.com/) is an all-in-one OS X GUI image optimizer. Imageoptim command line usage is possible with [an external program](https://code.google.com/p/imageoptim/issues/detail?can=2&start=0&num=100&q=&colspec=ID%20Type%20Status%20Priority%20Milestone%20Owner%20Summary%20Stars&groupby=&sort=&id=39).\n\n## The Future\n\nMaybe someday everyone will just use [AVIF](https://aomediacodec.github.io/av1-avif/) and [AV1](https://en.wikipedia.org/wiki/AV1) for everything and these sorts of tools will be obsolete. Or if Apple decides to support WebP it could happen even sooner.\n",
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajslater/picopt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
