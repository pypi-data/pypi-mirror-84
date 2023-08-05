import setuptools

setuptools.setup(
    name="hbv-scheduler",  # Replace with your own username
    version="0.0.1",
    author="Prashanth Mogali",
    author_email="m.prashanth54@gmail.com",
    description="Doctor patient home based visit routing and scheduling algorithm",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mprashanth54/home-visit-algorithm",
    packages=setuptools.find_packages(),
    # install_requires=['ortools', 'geopy'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
