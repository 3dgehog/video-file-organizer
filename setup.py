from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Video File Organizer',
    version='0.1b',
    python_requires='>=3.5',
    description="""Organizes the video files in the correct directories""",
    long_description=readme(),
    url='https://github.com/Scheercuzy/video_file_organizer',
    author='MX',
    author_email='maxi730@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vfo = video_file_organizer.__main__:main'
        ]
    },
    install_requires=[requirements]
)
