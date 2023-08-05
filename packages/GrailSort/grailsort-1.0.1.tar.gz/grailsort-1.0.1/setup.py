import setuptools

setuptools.setup(
    name = 'grailsort',
    version = '1.0.1',
    url = 'https://github.com/gaming32/grailsort',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'Cython wrapper around GrailSort (https://github.com/Mrrl/GrailSort)',
    long_description = '',
    long_description_content_type = 'text/markdown',
    # package_data = {
    #     'pygravity': [
    #         'py.typed',
    #         'math.pyi',
    #     ],
    #     'pygravity.twod': [
    #         'py.typed', 
    #         'vector.pyi',
    #         'physics.pyi',
    #         'gravity.pyi',
    #     ],
    # },
    # packages = [
    #     'pygravity',
    #     'pygravity.twod',
    # ],
    ext_modules = [
        setuptools.Extension('grailsort', ['grailsort.cpp']),
    ],
    py_modules = [
        'grailsort',
    ],
    zip_safe = False,
)
