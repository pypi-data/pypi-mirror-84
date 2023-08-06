from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='docker_cp',
    version='1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docker_cp=docker_cp:run',
        ],
    },
    url='https://www.github.com/galaxy102/docker_cp',
    license='MIT License',
    author='galaxy102',
    author_email='konstantin.koehring@gmail.com',
    description='Tool to use Docker Volumes with cp',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
