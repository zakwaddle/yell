import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yell',
    version='0.1.0',
    author='Zak',
    author_email='zakwaddle@gmail.com',
    description="A stylized developer console logger with themes and introspection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['yell'],
    install_requires=[],
    python_requires=">=3.7",
)
