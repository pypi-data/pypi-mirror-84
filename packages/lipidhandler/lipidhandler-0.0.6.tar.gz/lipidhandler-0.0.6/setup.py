from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='lipidhandler',
      version='0.0.6',
      description='Handle lipid names in Python.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/kaiserpreusse/lipidhandler',
      author='Martin Preusse',
      author_email='martin.preusse@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests'
      ],
      keywords=['LIPIDS', 'LIPIDOMICS'],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License'
      ],
      )
