import setuptools

setuptools.setup(
    name="sealpy",
    version="v0.0.1",
    license="GPLv3+",
    author="SEAL",
    description="Common non-R scripts and tools for SEAL",
    url="https://github.com/ncsuSEAL/commonCode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.4",
    entry_points={"console_scripts": ["hlsdownloader=hlsdownloader:main"]},
)
