from setuptools import setup, find_packages

setup(name='mathgenerator',
      version='1.1.5',
      description='An open source solution for generating math problems',
      url='https://github.com/todarith/mathgenerator',
      author='Luke Weiler',
      author_email='lukew25073@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['sympy', 'numpy', 'scipy'],
      entry_points={})
