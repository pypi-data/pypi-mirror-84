import setuptools

setuptools.setup(
    name="zacktools", # Replace with your own username
    version="0.0.1",
    author="Zack Dai",
    author_email="zdai@brocku.ca",
    description="Zack's common tools",
    long_description_content_type="text/markdown",
    url="https://github.com/ZackAnalysis/zacktools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['bs4','lxml','pyap~=0.3.1','requests']
)