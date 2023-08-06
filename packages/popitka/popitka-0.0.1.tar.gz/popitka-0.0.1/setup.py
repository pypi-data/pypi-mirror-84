from setuptools import setup, find_packages

def readme():
    with open('README.txt') as f:
        return f.read()

setup(name='popitka',
      version='0.0.1',
      description='Popitka package for training',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
      ],
      keywords='Popitka package',
      url='',
      author='Georgii Vasiukov',
      author_email='vasyukov.georgiy.yu@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[''],
      include_package_data=True,
      zip_safe=False)