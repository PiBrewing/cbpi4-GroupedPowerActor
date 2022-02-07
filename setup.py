from setuptools import setup

setup(name='cbpi4-GroupedPowerActor',
      version='0.0.3',
      description='CraftBeerPi Plugin',
      author='',
      author_email='',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-GroupedPowerActor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-GroupedPowerActor'],
     )
