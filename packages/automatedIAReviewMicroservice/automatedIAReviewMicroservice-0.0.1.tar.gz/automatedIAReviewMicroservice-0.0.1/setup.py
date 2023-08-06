from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Automated Intenal Audit Review Package'
LONG_DESCRIPTION = 'Automated Intenal Audit Review Package'

# Setting up
setup(
    name="automatedIAReviewMicroservice",
    version=VERSION,
    author="Stephen Sanwo",
    author_email="stephen.sanwo@icloud.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'internal audit', 'risk', 'compliance'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
