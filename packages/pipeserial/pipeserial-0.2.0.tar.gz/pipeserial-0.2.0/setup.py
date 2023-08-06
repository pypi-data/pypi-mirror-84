# type: ignore
"""PipeSerial setup.py for setuptools.

Source code available at https://github.com/tykling/pipeserial/
Can be installed from PyPi https://pypi.org/project/pipeserial/
Read more at https://pipeserial.readthedocs.io/en/latest/
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pipeserial",
    version="0.2.0",
    author="Thomas Steen Rasmussen",
    author_email="thomas@gibfest.dk",
    description="PipeSerial is a command-line utility to send some input from stdin to a serial device, and then collect and return the output from the device.",
    license="BSD License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tykling/pipeserial",
    packages=["pipeserial"],
    entry_points={"console_scripts": ["pipeserial = pipeserial.pipeserial:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["pyserial", "pexpect", "pexpect_serial"],
    include_package_data=True,
)
