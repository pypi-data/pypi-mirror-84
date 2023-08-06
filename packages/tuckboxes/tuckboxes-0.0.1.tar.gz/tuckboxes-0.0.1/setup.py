from setuptools import setup, find_packages

version = '0.0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tuckboxes",
    version=version,
    entry_points={
        'console_scripts': [
            "tuckboxes = tuckboxes.tuckboxes:main"
        ],
    },
    packages=find_packages(exclude=['tests']),
    install_requires=["reportlab>=3.4.0",
                      "Pillow>=4.1.0",
                      "numpy"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://domtabs.sandflea.org',
    include_package_data=True,
    author="Peter Gorniak",
    author_email="sumpfork@mailmight.net",
    description="Tuckbox Generation for Board- and Cardgames",
    keywords=['boardgame', 'cardgame', 'tuckboxes'],
)
