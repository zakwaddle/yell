from setuptools import setup, find_packages

setup(
    name='yell',
    version='0.1.2',
    url='https://github.com/zakwaddle/yell',
    packages=find_packages(where="."),
    package_dir={"": "."},
    description="A stylized developer console logger with themes and introspection.",
    author='Zak',
    author_email='zakwaddle@gmail.com',
    install_requires=[],
    python_requires=">=3.7",
)
