import os
from setuptools import setup

path = os.path.dirname(__file__)
long_desc_fd = os.path.join(path, 'README.md')

long_description = ''

with open(long_desc_fd) as f:
    long_description = f.read()

setup(
    name='huntress',
    version='0.0.1',
    packages=['huntress'],
    url='https://github.com/sillyfatcat/huntress',
    license='MIT',
    author='stupidfatcat',
    author_email='sshum@stupidfatcat.com',
    description='Educational package about throwing hatchets and learning how to push code to PyPi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['EDUCATIONAL', ],
    download_url='https://github.com/sillyfatcat/huntress/archive/v0.1.tar.gz',
    install_requires=[
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': ['huntress=huntress.main:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)