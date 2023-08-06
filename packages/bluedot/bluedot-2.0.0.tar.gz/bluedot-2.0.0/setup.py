import sys
from setuptools import setup

if sys.version_info.major == 2:
    raise ValueError('This package does not support Python 2')
elif sys.version_info.major == 3:
    if sys.version_info.minor < 5:
        raise ValueError('This package requires Python 3.5 or newer')
else:
    raise ValueError('Python version not identified')

__project__ = 'bluedot'
__desc__ = 'A zero boiler plate bluetooth remote'
__version__ = '2.0.0'
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin@ohanlonweb.com'
__license__ = 'MIT'
__url__ = 'https://github.com/martinohanlon/BlueDot'
__python_requires__ = '>=3.5'
# __requires__ = ['dbus-python',]
__keywords__ = [
    "raspberry",
    "pi",
    "raspberry pi",
    "bluetooth",
    "remote",
    "android",
]
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Communications",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]
__long_description__ = """# Blue Dot

[Blue Dot](http://bluedot.readthedocs.io/en/latest/) allows you to control your Raspberry Pi projects wirelessly - it's a Bluetooth remote and zero boiler plate (super simple to use :) Python library.

## Getting started

1. Install

```
sudo pip3 install bluedot
```

2. Get the [Android Blue Dot app](http://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot) or use the [Python Blue Dot app](http://bluedot.readthedocs.io/en/latest/bluedotpythonapp.html)

3. Pair your Raspberry Pi

4. Write some code

```python
from bluedot import BlueDot
bd = BlueDot()
bd.wait_for_press()
print("You pressed the blue dot!")
```

5. Press the Blue Dot

See the [getting started guide](http://bluedot.readthedocs.io/en/latest/gettingstarted.html) to 'get started'!

## More

Blue Dot is more than just one button. You can create as many buttons as you want and change their appearance to create your own controller.

Every button is also a joystick. You can tell if a button was pressed in the middle, on the top, bottom, left or right. You can easily create a BlueDot controlled Robot.

Why be restricted by such vague positions like top and bottom though: you can get the exact (x, y) position or even the angle and distance from centre where the button was pressed.

Its not all about when the button was pressed either - pressed, released or moved they all work.

A button can be any colour, square, given give or hidden!

You can press it, slide it, swipe it, rotate it - one blue circle can do a lot!

## Even more

The [online documentation](http://bluedot.readthedocs.io/en/latest/) describes how to use Blue Dot and the Python library including recipes and ideas.

"""
if __name__ == '__main__':
    setup(name='bluedot',
        version = __version__,
        description = __desc__,
        long_description=__long_description__,
        long_description_content_type='text/markdown',
        url = __url__,
        author = __author__,
        author_email = __author_email__,
        license= __license__,
        keywords=__keywords__,
        classifiers=__classifiers__,
        packages = [__project__],
        # install_requires = __requires__,
        entry_points={
            'console_scripts': [
                'bluedotapp = bluedot.app:main'
                ]},
        )
