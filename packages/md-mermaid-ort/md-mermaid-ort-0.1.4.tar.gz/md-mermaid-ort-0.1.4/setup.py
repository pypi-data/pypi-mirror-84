from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='md-mermaid-ort',
    version='0.1.4',
    author='Olivier Robardet',
    author_email='olivier.robardet@gmail.com',
    description='Fork of original md_mermaid by Olivier Ruelle, including some fixes with PR awaiting on the upstream',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/orobardet/md_mermaid',
    py_modules=['md-mermaid-ort'],
    install_requires = ['markdown>=2.5'],
    python_requires='>=3',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
