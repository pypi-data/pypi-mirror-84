from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 8.1',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pydevtoolkit',
    version='0.0.2',
    description='A python toolkit for developers',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Snowflake',
    author_email='snowflake@fake.com',
    license='MIT',
    classifiers=classifiers,
    keywords='py_tk',
    packages=find_packages(),
    install_requires=['']
)
