import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FormulaBasedMaterials", # Replace with your own username
    version="v0.1.0a2",
    author="Michael, Yu-Chuan, Hsu",
    author_email="mk60503mk60503@gmail.com",
    description="A code for generating Formula-Based Materials into Voxel, STL files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MicDonald/FormulaBasedMaterials/archive/v0.1.0.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'trimesh',
        'time',
        'warnings',
        'skimage',
        'random',
        'sympy',
      ],
    python_requires='>=3.6',
)