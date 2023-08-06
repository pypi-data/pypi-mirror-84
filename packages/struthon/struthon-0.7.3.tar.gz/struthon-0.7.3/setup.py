from distutils.core import setup

setup(
    name='struthon',
    version='0.7.3',
    description='structural engineering design python applications',
    long_description = open("README.rst").read(),
    author='Lukasz Laba',
    author_email='lukaszlaba@gmail.com',
    url='https://bitbucket.org/struthonteam/struthon',
    packages=[  'struthon', 
                'struthon.ConcreteMonoSection', 
                'struthon.ConcretePanel', 'struthon.ConcretePanel.Example_data_files',
                 'struthon.SteelSectionBrowser', 
                 'struthon.SteelMember',
                 'struthon.SteelBoltedConnection'],
    package_data = {'': ['*.xls', '*.csv']},
    license = 'GNU General Public License (GPL)',
    keywords = 'civil engineering ,structural engineering, concrete structures, steel structures',
    python_requires='>=3.5, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    )
    