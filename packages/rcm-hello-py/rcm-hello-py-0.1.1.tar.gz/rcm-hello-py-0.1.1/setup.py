#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

import setuptools

setuptools.setup(
    name="rcm-hello-py",
    version="0.1.1",
    author="Pim Hazebroek",
    author_email="author@example.com",
    description="A dummy python project for testing",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/residential-climate-monitoring/hello-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
