import setuptools

setuptools.setup(
    name='docsvault',
    version='0.1.1',
    author='Sylvan Le Deunff',
    author_email='sledeunf@gmail.com',
    description='Web app used to securely version your documents on git',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='docsvault, documents, store, vault',

    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'dvault = docsvault.__main__:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/sylvan-le-deunff/docsvault/issues',
        'Source': 'https://github.com/sylvan-le-deunff/docsvault',
        #'Funding': 'https://donate.pypi.org',
        #'Say Thanks!': 'http://saythanks.io/to/example',
    },
)
