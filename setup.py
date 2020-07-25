from setuptools import setup

setup(
    name='cow',
    version='1.1.1',
    packages=['cow',
              'cow.streamlit_',
              'cow.logging_'
              ],
    zip_safe=False,
    install_requires=['PyYaml', 'requests', 'rsa', 'ntplib==0.3.4', 'pytz', "colorlog"]
)
