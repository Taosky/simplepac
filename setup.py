from setuptools import setup

setup(name='simplepac',
      version='0.1',
      description='Generate pac simply',
      url='https://github.com/Taosky/simplepac',
      author='Taosky',
      author_email='t@firefoxcn.net',
      license='MIT',
      packages=['simplepac'],
      package_data={
          'simplepac': ['resources/*']
      },
      entry_points={
          'console_scripts': ['simplepac=simplepac.core:run'],
      },
      install_requires=[
          'requests',
          'matplotlib',
          'numpy',
          'sklearn',
          'scipy ',
      ],
      zip_safe=False)
