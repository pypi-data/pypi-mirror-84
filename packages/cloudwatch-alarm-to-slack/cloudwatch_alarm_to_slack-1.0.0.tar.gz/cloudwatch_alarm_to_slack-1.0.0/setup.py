#!/usr/bin/env python

"""The setup script."""

import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

requirements = [
      'slack-sdk',
      'pydantic'
]

setuptools.setup(
      author='Jermila Paul Dhas',
      author_email='dhas.jermila@gmail.com',
      description='A python library to send cloudwatch alarm events from sns to slack',
      url='https://github.com/jpdhas/cloudwatch_alarm_to_slack',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT license',
      name='cloudwatch_alarm_to_slack',
      version='1.0.0',
      python_requires='>=3.6',
      install_requires=requirements,
      packages=setuptools.find_packages(),
      include_package_data=True,
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Software Development",
      ],
      keywords=[
            "cloudwatch_alarm_to_slack",
            "cloudwatchalarm",
            "sns",
            "slack",
            "lambda"
      ],
      zip_safe=False
)
