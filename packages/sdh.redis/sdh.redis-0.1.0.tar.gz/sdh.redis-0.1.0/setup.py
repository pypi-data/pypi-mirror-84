from setuptools import find_packages, setup

version = '0.1.0'

needed = [
    'redis>=3.5.0',
    'Django>=2.2.0'
]

setup(
    name='sdh.redis',
    version=version,
    url='https://bitbucket.org/sdh-llc/sdh-redis/',
    author='Software Development Hub LLC',
    author_email='dev-tools@sdh.com.ua',
    description='Django redis wrapper',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sdh'],
    eager_resources=['sdh'],
    include_package_data=True,
    entry_points={},
    zip_safe=False,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
