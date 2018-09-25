import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="satsp",
    version="0.7",
    url="https://github.com/hcluo/satsp",
	
    author="Haochen Luo",
    author_email="hcluo92@gmail.com",
	
	
    description="Travelling Salesman Problem Using Simulated Annealing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(),
	
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
