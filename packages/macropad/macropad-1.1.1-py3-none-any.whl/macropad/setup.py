from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]


setup(
    name="macropad",
    version="1.0",
    description="Use the LaunchpadMk2 as a Macro Device",
    author="LiquidDevect",
    license="MIT",
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=["launchpad_py", " pygame"]
)