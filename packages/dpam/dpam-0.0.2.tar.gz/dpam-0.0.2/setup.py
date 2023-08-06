import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

data_files = {}
data_files['dpam'] = []

directories = os.listdir('/n/fs/percepaudio/PerceptualAudio/dpam/pre-model/')
for directory in directories:
    for direc2 in os.listdir(os.path.join('/n/fs/percepaudio/PerceptualAudio/dpam/pre-model/',directory)):
        data_files['dpam'].append(os.path.join('/n/fs/percepaudio/PerceptualAudio/dpam/pre-model/',directory,direc2))

print(data_files)
setuptools.setup(
    name="dpam", # Replace with your own username
    version="0.0.2",
    author="Pranay Manocha",
    author_email="pranaymnch@gmail.com",
    description="A pip package for perceptual audio metric",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pranaymanocha/PerceptualAudio",
    packages=setuptools.find_packages(),
    package_data=data_files,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)