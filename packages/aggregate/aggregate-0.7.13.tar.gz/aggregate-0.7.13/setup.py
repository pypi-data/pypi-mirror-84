# https://pythonhosted.org/an_example_pypi_project/setuptools.html
# set HOME=c:\s\telos\python
# python setup.py sdist bdist_wininst upload.bat
# pip freeze > file to list installed packages
# pip install -r requirements.txt to install

from setuptools import setup
import os
from time import time

tests_require = ['unittest', 'sly']
install_requires = [
    'pypandoc',
    'sly==0.3',
    'scipy',
    'seaborn',
    'matplotlib',
    'numpy'
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


long_description = read('README.rst')


def version_number():
    with open('version_number.md', 'r') as f:
        t = f.read()
    lt = t.split('\n')
    last_update = float(lt[1])
    # updates at least one hour apart
    if time() - last_update > 60 * 60:
        s = lt[0].strip().split('.')
        n = int(s[-1])
        s[-1] = str(n+1)
        t = '.'.join(s)
        with open('version_number.md', 'w') as f:
            f.write(f'{t}\n{time()}')
            print(f'Updated version number to {t}')
    else:
        t = lt[0].strip()
        print('No change')
    return t

# agg/*.agg is the parameter and curve files

setup(name="aggregate",
      description="aggregate - working with compound probability distributions",
      long_description=long_description,
      license="""BSD""",
      version=version_number(),
      author="Stephen J. Mildenhall",
      author_email="steve@convexrisk.com",
      maintainer="Stephen J. Mildenhall",
      maintainer_email="steve@convexrisk.com",
      packages=['aggregate'],
      package_data={'': ['*.txt', '*.rst', '*.md', 'agg/*.agg', 'examples/*.py', 'examples/*.ipynb',
                         'test/*.py']},
      tests_require=tests_require,
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: BSD License',
          'Topic :: Education',
          'Topic :: Office/Business :: Financial',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Education'
      ],
      project_urls={"Documentation": 'https://aggregate.readthedocs.io/en/latest/',
                    "Source Code": "https://github.com/mynl/aggregate_project"}
      )
