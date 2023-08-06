
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="joystickduino",
    version="0.0.1",
    author='Someone',
    author_email="shaurya.p.singh21@gmail.com",
    description="may the force be with you",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyserial',
        'pyautogui'
    ]
)
