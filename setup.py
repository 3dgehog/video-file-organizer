from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="Video File Organizer",
    version="2",
    python_requires=">=3.6",
    description="""Organizes the video files in the correct directories""",
    long_description=readme(),
    url="https://github.com/Scheercuzy/video_file_organizer",
    author="MX",
    author_email="maxi730@gmail.com",
    license="MIT",
    install_requires=[
        "babelfish==0.5.5",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "flask==1.1.2",
        "guessit==3.1.1",
        "itsdangerous==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jaraco.functools==3.0.1; python_version >= '3.6'",
        "jinja2==2.11.2",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "more-itertools==8.4.0; python_version >= '3.5'",
        "pyaml==20.4.0",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2020.1",
        "pyyaml==5.3.1",
        "rebulk==2.0.1",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "tempora==4.0.0; python_version >= '3.6'",
        "uwsgi==2.0.19.1",
        "werkzeug==1.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "yg-lockfile==2.3",
        "zc.lockfile==2.0",
    ],
    dependency_links=[],
    packages=["video_file_organizer"],
    include_package_data=True,
    entry_points={"console_scripts": ["vfo = video_file_organizer.__main__:main"]},
)
