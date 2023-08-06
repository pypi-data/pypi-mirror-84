from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.0.1'

setup(
    name="chitboxes",
    version=version,
    entry_points={
        'console_scripts': [
            "chitboxes = chitboxes.chitboxes:main"
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
    description="Chitbox Generation for Board- and Cardgames",
    keywords=['boardgame', 'cardgame', 'chitboxes']
)
