from setuptools import setup, find_packages

setup(
    name='application-config',
    version='0.0.1',
    python_requires='>=3.6',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    url='https://github.com/bholten/py-application-config',
    license='MIT',
    author='Brennan Holten',
    author_email='brennan.holten@objectpartners.com',
    description='Simple decorator for injecting a configuration into classes',
    install_requires=['PyYAML']
)
