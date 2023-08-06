from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='scipy-tweaks',
      version='0.1.1',
      description='Utility functions for scipy.',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/ulf1/scipy-tweaks',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['scipy_tweaks'],
      install_requires=[
          'setuptools>=40.0.0',
          'scipy>=1.5.4'],
      python_requires='>=3.6',
      zip_safe=False)
