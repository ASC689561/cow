from setuptools import setup

setup(
    name='cow',
    version='1.1.1',
    packages=['cow',
              'cow.patterns',
              'cow.patterns.observer',
              'cow.patterns.visitor',
              'cow.streamlit_'
              ],
    zip_safe=False,
    install_requires=['requests', 'rsa', 'ntplib==0.3.4', 'pytz', 'python-logstash-async', "colorlog"]
)
