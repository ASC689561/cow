from setuptools import setup

setup(
    name='cow',
    version='1.1.1',
    packages=['cow', 'cow.patterns','cow.patterns.observer','cow.patterns.singleton','cow.patterns.visitor'],
    zip_safe=False,
    install_requires=['requests']
)
