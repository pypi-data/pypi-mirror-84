from setuptools import setup, find_packages

with open('README.txt') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="fuzzy_pratish",
    version="0.2",
    description="A python package to handle fuzzy operations",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    author="Pratish Tiwari",
    author_email="pratishtiwari1@gmail.com",
    url = "https://github.com/PratishTiwari/DL_modules",
    include_package_data=True
)

install_requires=[
        "numpy>=1.18.5",
        "pandas>=1.0.5",
        "scikit-learn>=0.23.1",      
]

if __name__=='__main__':
    setup(**setup_args, install_requires=install_requires)