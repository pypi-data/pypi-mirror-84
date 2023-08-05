import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hiegeo",
    version="0.1.7",
    author="Alessandro Comunian",
    author_email="alessandro.comunian@unimi.it",
    description="Modelling stratigraphic alluvial architectures, constrained by stratigraphic hierarchy and relative chronology",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://bitbucket.org/alecomunian/hiegeo",
    packages=['hiegeo'],
    py_modules=["hiegeo"],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering'
    ],
    keywords = "geology, modelling, hierarchy, chronology",
    project_urls = {
        'Documentation': 'https://hiegeo.readthedocs.io/en/latest/index.html',
        'Source': 'https://bitbucket.org/alecomunian/hiegeo',
        },
    
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "matplotlib",
        "anytree",
        "pandas"],
    package_dir = {"": "."},
)


