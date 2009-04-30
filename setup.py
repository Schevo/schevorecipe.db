from setuptools import setup, find_packages

setup(
    name='schevorecipe.db',
    author='ElevenCraft Inc.',
    author_email='schevo@googlegroups.com',
    description='zc.buildout recipe(s) for managing Schevo databases',
    version='0.1',
    url='http://www.schevo.org/',
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    namespace_packages=[
        'schevorecipe',
    ],
    packages=find_packages(exclude=['ez_setup']),
    entry_points={
        'zc.buildout': [
            'default = schevorecipe.db.recipe:Recipe',
        ],
    },
    classifiers=[
        'Environment :: Plugins',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Installation/Setup',
        'License :: OSI Approved :: BSD License',
    ],
)
