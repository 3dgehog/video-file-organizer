from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="video-file-organizer",
    version="2",
    python_requires=">=3.6",
    description="""Organizes the video files in the correct directories""",
    long_description=readme(),
    url="https://github.com/Scheercuzy/video_file_organizer",
    author="MX",
    author_email="maxi730@gmail.com",
    license="MIT",
    install_requires=[
        "apscheduler==3.7.0",
        "babelfish==0.5.5",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "filelock==3.0.12",
        "flask==1.1.2",
        "greenlet==1.0.0; python_version >= '3'",
        "guessit==3.3.1",
        "importlib-metadata==3.9.0; python_version < '3.8'",
        "itsdangerous==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jinja2==2.11.3",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "plumbum==1.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "pyaml==20.4.0",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2021.1",
        "pyyaml==5.4.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
        "rebulk==3.0.1",
        "redis==3.5.3",
        "rpyc==5.0.1",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sqlalchemy==1.4.3",
        "supervisor==4.2.2",
        "typing-extensions==3.7.4.3; python_version < '3.8'",
        "tzlocal==2.1",
        "uwsgi==2.0.19.1",
        "werkzeug==1.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "zipp==3.4.1; python_version >= '3.6'",
    ],
    dependency_links=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["vfo = video_file_organizer.__main__:main"]},
)
