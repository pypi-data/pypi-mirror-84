import os
from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="cir-alerts",
    version="0.0.1",
    author="Paweł Samoraj",
    author_email="samoraj.pawel@gmail.com",
    description="cir-alerts prototype",
    url="http://packages.python.org/cir-alerts",
    packages=['cir_alerts', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)
