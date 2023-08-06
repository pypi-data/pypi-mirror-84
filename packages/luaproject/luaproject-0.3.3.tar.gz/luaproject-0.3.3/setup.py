import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]


setup(
    name="luaproject",
    version="0.3.3",
    description="Use python package to manage LUA plugin, so that the plugin can be published to private pypi server and used internally. A temporary solution for PYTHONER using kong.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    url="https://github.com/zencore-cn/zencore-issues",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["luaproject"],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["luaproject"],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "luaproject = luaproject.cli:main",
        ],
    },
)