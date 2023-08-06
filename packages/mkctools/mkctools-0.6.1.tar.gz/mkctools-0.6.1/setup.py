import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='mkctools',
    version='0.6.1',
    description='Machine Learning Libraries',
    author='Michael Chen',
    author_email='mc6666@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/mc6666/mkctools',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',)