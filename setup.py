from setuptools import setup
from enscli import __version__

setup(
    name='enlightns-cli',
    version=__version__,
    description='EnlightNS.com Command Line Interface.',
    # long_description=readme + '\n\n' + history,
    author='Dominick Rivard',
    author_email='support@enlightns.com',
    url='http://enlightns.com/',
    py_modules=['enscli'],  # List the modules within the enlightns-cli project.
    include_package_data=True,
    license='Apache 2.0',
    zip_safe=False,classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
    install_requires=[
        'click==4.0',
    ],
    entry_points='''
        [console_scripts]
        enlightns-cli=cli:cli
    ''',
)
