from distutils.core import setup

setup(
    name='keepboo-bookmarksparser',
    version='0.0.1',
    packages=['keepoo_bookmarksparser'],
    url='https://github.com/KEEPBOO/bookmarks-parser',
    license='',
    author='Oleg Stasula',
    author_email='oleg.stasula@gmail.com',
    description='Parser is used on KEEPBOO to parse bookmarks.html file',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    keywords='keepboo parser',
    install_requires=[
        'beautifulsoup4'
    ],
)
