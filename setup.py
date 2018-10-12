from setuptools import setup


setup(
    name = 'rpi_server',
    version = '0',
    setup_requires=["pytest-runner", 'RPi.GPIO',],
    tests_require=['pytest>=3.8.2',],
)
