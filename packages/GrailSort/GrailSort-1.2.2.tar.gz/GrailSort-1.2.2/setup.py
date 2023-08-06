import setuptools

with open('README.md') as fp:
    long_description = fp.read()

setuptools.setup(
    name = 'GrailSort',
    version = '1.2.2',
    url = 'https://github.com/gaming32/grailsort',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'Cython wrapper around GrailSort (https://github.com/gaming32/GrailSort-Maintained)',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    ext_modules = [
        setuptools.Extension('grailsort', ['grailsort.cpp']),
        setuptools.Extension('cGrailSort', ['cGrailSort.cpp']),
    ],
    zip_safe = False,
)
