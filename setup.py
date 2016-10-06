from setuptools import setup
setup(
    name = "t2",
    version = "0.0.1",
    author = "Collin Richards",
    author_email = "richardscollin@gatech.edu",
    description = ("A command line interface to t-square."),
    license = "MIT",
    keywords = "t2 t-square saiki",
    url = "http://github.com/lugatgt/t2",
    packages=['t2'],
    scripts=['scripts/t2'],
    install_requires=['selenium', 'click'],
)
