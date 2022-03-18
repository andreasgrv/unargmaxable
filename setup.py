from setuptools import setup, find_packages

setup(
      name='stollen',
      packages=find_packages(include=['stollen', 'stollen.*']),
      version='0.0.1',
      description='Stollen probability',
      license='BSD',
      keywords=['Softmax bottleneck'],
      scripts=['bin/stollen_random',
               'bin/stollen_numpy',
               'bin/stollen_hugging',
               'bin/stollen_prevention'],
      classifiers=[],
      tests_require=['pytest']
)
