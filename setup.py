import sys
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')
    
setup(
    name='labbot',
    packages=['labbot'],
    include_package_data=True,
    version='1.0.0',
    url='https://www.jmaclabs.com',
    author='John MacDonald',
    author_email='john@jmaclabs.com',
    description='JMacLabs LabBot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "slack_sdk>=3.0",
        "slackeventsapi>=2.1.0",
        "Flask>=1.1.2",
        "python-dotenv>=0.17.1"
    ],
    python_requires='>=3.6'
)