import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hbv-scheduler-mprashanth54",  # Replace with your own username
    version="0.0.1",
    author="Prashanth Mogali",
    author_email="m.prashanth54@gmail.com",
    description="Doctor patient home based visit routing and scheduling algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mprashanth54/home-visit-algorithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
