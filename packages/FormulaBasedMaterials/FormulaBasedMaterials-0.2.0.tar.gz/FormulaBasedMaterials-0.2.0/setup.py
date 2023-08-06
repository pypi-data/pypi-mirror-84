import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FormulaBasedMaterials", # Replace with your own username
    version="0.2.0",
    license='MIT',
    author="Michael, Yu-Chuan, Hsu",
    author_email="mk60503mk60503@gmail.com",
    description="A code for generating Formula-Based Materials into Voxel, STL files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['Formula-Based', '3D printing', 'stl', 'voxel', 'surface'],
    url="https://github.com/MicDonald/FormulaBasedMaterials",
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
        'scikit-image',
        'sympy',
      ],
    python_requires='>=3.6',
)