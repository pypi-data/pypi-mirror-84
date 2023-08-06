import setuptools

setuptools.setup(
    name="streaming-common",
    version="0.0.1",
    description="Model structure that the data gets converted to before serialization into Kinesis stream.",
    url="https://github.com/seniorplanning/streaming-common",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)