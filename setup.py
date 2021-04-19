from setuptools import setup, find_packages


setup(
    name='mkdocs-thumbnails',
    version='0.1.0',
    description='A MkDocs plugin.  Generates thumbnails for links in the markdown',
    long_description='',
    keywords='mkdocs',
    url='',
    author='Norman Lorrain ',
    author_email='normanlorrain@gmail.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.0.4',
        'Pillow>=8.2.0',
        'PyMuPDF>=1.18.12'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'thumbnails = thumbnails.plugin:ThumbnailMaker'
        ]
    }
)
