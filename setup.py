from setuptools import setup
from meta import __version__

setup(
    name='mergeyaml',
    version=__version__,
    author="Erik Olson",
    py_modules=['mergeyaml'],
    license="MIT",
    install_requires=[
        "click==6.7",
        "PyYAML==3.12",
        "oyaml>=0.4",
    ],
    entry_points='''
        [console_scripts]
        mergeyaml=mergeyaml:cli
    ''',
)
