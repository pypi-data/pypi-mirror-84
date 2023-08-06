import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BluetoothLEpkgaiqi",
    version="1.0.1",
    author="liumingming",
    author_email="994505261@eqq.com",
    description="A BluetoothLE  in Windows 10 V2004",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    url='https://www.python.org/',
    packages=setuptools.find_packages(),
 

    package_data = {
        # 任何包中含有.dll文件，都包含它
        '': ['*.dll'],
    
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
         'pythonnet >=2.5.1',
     ],
  

)