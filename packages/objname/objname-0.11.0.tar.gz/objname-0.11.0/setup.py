from setuptools import setup  # type: ignore[import]


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="objname",
    version="0.11.0",
    packages=["objname"],
    package_data={
        "objname": ["__init__.py", "py.typed", "_module.py",
                    "test_objname.py"],
    },

    zip_safe=False,
    author="Alan Cristhian Ruiz",
    author_email="alan.cristh@gmail.com",
    description="A library with a base class that "
                "stores the assigned name of an object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Software Development :: Object Brokering',
        'Typing :: Typed'
      ],
    license="MIT",
    keywords="data structure debug",
    url="https://github.com/AlanCristhian/objname",
)
