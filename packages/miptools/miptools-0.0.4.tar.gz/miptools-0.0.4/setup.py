from setuptools import setup

setup(name='miptools',
      version='0.0.4',
      description='miptools is a preprocessing utility that allows users to preprocess medical images at ease',
      url='https://github.com/chinokenochkan/miptools',
      author='Chi Nok Enoch Kan',
      author_email='chinokenoch.kan@marquette.edu',
      license='MIT',
      packages=['miptools'],
      install_requires=[
          'pydicom','numpy','matplotlib','scipy'
      ],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      zip_safe=False)