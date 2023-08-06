from setuptools import setup

from ciscoglass import __version__

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='ciscoglass',
    version=__version__,
    description='Wrapper/SDK for Cisco Glass Apps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://wwwin-github.cisco.com/ciscoglass/python-sdk.git',
    author='Adyanth H',
    author_email='adyah@cisco.com',
    # license='BSD 2-clause',
    packages=['ciscoglass'],
    install_requires=['requests', 'click'],

    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Intended Audience :: Science/Research',
        # 'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.8',
    ],
)
