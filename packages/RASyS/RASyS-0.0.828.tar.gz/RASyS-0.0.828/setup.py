from distutils.core import setup


def readme():
    with open('README.md') as file:
        README = file.read()
        return README


setup(
    name='RASyS',
    packages=['RASyS'],
    version='0.0.828',
    license='MIT',
    description='RASyS is a powerful package of python.',
    long_description=readme(),
    author='RaviARS',
    author_email='ravi8ars28@gmail.com',
    url='https://github.com/raviars',
    keywords=['ARS', 'RAVIARS', 'ARS28', "RASyS"],
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
