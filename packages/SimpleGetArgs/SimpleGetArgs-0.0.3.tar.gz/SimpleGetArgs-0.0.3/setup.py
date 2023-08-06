from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Bug Tracking',
          ]


setup(name='SimpleGetArgs',
      version='0.0.3',
      description='Test to Publish the Command Line',
      py_modules=["GetArgs"],
      # package_dir={'': 'src'},
      entry_points={'console_scripts': ['GetArgs = GetArgs.__main__:main']},
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='MSBeni',
      author_email='andrei.sokurov.bitco@gmail.com',
      # License='MIT',
      classifiers=classifiers,
      keywords='calculator',
      url='https://github.com/MSBeni/PublishArgparse',
      packages=find_packages(),
      # install_requiers=[''],
      extras_require={
          "dev": [
              "pytest>=3.7",
          ],
      }
     )


