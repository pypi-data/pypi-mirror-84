import io
from setuptools import setup

setup(name='NotSoFastQC',
      description='A tool to generate FastQC-like graphs from a FastQC file',
      long_description=io.open('README.md', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      version='1.1',
      url='https://github.com/jamesfox96/NotSoFastQC',
      packages=['NotSoFastQC'],
      install_requires=['tabulate>=0.8.7',
                        'pandas>=0.25.0rc0',
                        'matplotlib>=3.3.2',
                        'seaborn>=0.11.0',
                        'numpy>=1.17.0rc1',
                        'scipy>=1.5.4'],
      entry_points={'console_scripts': ['NotSoFastQC=NotSoFastQC.__main__:main']},
      )
