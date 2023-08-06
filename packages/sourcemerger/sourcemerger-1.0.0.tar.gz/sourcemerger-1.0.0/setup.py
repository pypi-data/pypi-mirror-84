import setuptools
from source.sourcemerger import _version

setuptools.setup(name='sourcemerger',
                 package_dir={'': 'source'},
                 packages=setuptools.find_packages(where='source'),
                 version=_version,
                 description='sourcemerger is a command-line tool that generates '
                             'a single-header C++ library from your source code.',
                 long_description=open('readme.md').read(),
                 long_description_content_type='text/markdown',
                 url='https://gitlab.com/russofrancesco/sourcemerger',
                 author='Francesco Russo',
                 author_email='sourcemerger@frusso.dev',
                 license='MIT License',
                 classifiers=[
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: C++',
                     'Operating System :: OS Independent',
                     'Intended Audience :: Developers',
                     'Topic :: Utilities'
                 ],
                 keywords=[
                     'sourcemerger', 'c++', 'single-header',
                     'library', 'concatenate', 'merge'],
                 python_requires='~=3.6',
                 entry_points={
                     'console_scripts': [
                         'sourcemerger=sourcemerger:_cmdline_tool_main'
                     ],
                 }
                 )
