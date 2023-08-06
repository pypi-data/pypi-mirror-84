import os

import requests
from setuptools import setup, find_packages


def md_to_rst(from_file, to_file):
    res = requests.post(url='http://c.docverter.com/convert',
                        data={'to': 'rst', 'from': 'markdown'},
                        files={'input_files[]': open(from_file, 'rb')})
    if res.ok:
        with open(to_file, "wb") as f:
            f.write(res.content)


md_to_rst("README.md", "README.rst")

setup(
    name='feishu-sdk-py',
    version='0.0.1',
    description='Feishu Python SDK',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    python_requires='>=3.4',
    url='https://github.com/Thoxvi/feishu-sdk-py',
    author='Thoxvi',
    author_email='A@Thoxvi.com',
    install_requires=[
        "requests"
    ],
    keywords='api feishu sdk python 996-icu-license pypi pypi-source',
    packages=find_packages(),
)
