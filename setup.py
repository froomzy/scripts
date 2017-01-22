from setuptools import setup

setup(name='scripts',
      version='0.1',
      description='A set of scripts frop deploying my apps to their servers,',
      url='https://github.com/froomzy/scripts',
      author='Dylan Jenkinson',
      author_email='dylan@dylan-jenkinson.nz',
      license='MIT',
      packages=['scripts'],
      install_requires=[
          'Fabric3',
          'PyYAML',
          'petname',
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'deploy=scripts.bin.deploy:main'
          ]
      }
)
