from distutils.core import setup


with open('README.rst') as f:
    readme = f.read()

setup(
    name = 'KnightAttackOrcs',
    version= '2.0.0',
    packages=['wargame'],
    url = "https://https://test.pypi.org/legacy/KnightAttackOrcs",
    license='LICENSE.txt',
    description='fantasy game',
    long_description=readme,
    author='Dominery',
    author_email='18758205238@163.com'
)