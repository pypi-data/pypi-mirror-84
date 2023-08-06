from setuptools import setup

def long_desc():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()

setup(name='rus2latin_date',
      version='1.2',
      description='Utility for converting Russian date into Roman',
      long_description=long_desc(),
      classifiers=[
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Developers'
      ],
      author='Boris Orekhov',
      license="GPL",
      keywords='nlp dates russian latin calendar',
      author_email='nevmenandr@gmail.com',
      url='https://github.com/nevmenandr/rus2latin_date',
      packages=['rus2latin_date'],
      install_requires=[
          'rutimeparser'
      ],
      include_package_data=True,
      zip_safe=False)