from setuptools import setup, find_packages

setup(name='KorFeatures',
      version='0.1',
      description='Analyze features for Kor projects',
      url='http://github.com/seantyh/KorFeatures',
      author='Sean Tseng',
      author_email='seantyh@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy'],
      zip_safe=False)

