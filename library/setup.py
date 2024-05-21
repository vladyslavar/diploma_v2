from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Error handling library'
LONG_DESCRIPTION = 'Diploma project. Error handling library for Python.'

setup(
        name="error_handler_diploma", 
        version=VERSION,
        author="Vladyslava Rozhkovan",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'error handling', 'library', 'diploma project'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)