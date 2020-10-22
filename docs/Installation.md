# Installation

## For Development

Clone the directory with git then:

```bash
cd video_file_organizer
pipenv install
```

### Setting up config files

Before automizing the program, the setup config and rule book need to be setup. Run the program once using `--create-config` flag to get empty config files created in the current directory

```bash
vfo --create-config
```

## For Production

## SystemD

Use the toolbox included to do so, run:

```bash
pipenv run python toolbox.py --systemd
```

2 systemd files will be located in a newly created folder called `systemd/`. You simply have to link those files to systemd by:

```bash
cd systemd
sudo systemctl link ${PWD}/vfo.service
sudo systemctl enable ${PWD}/vfo.timer
sudo systemctl start vfo.timer
```

## Docker

Build Webserver

```bash
docker build . -f video_file_organizer_webserver/Dockerfile --tag video_file_organizer_webserver:latest
```

Build Scheduler

```bash
docker build . -f video_file_organizer_scheduler/Dockerfile --tag video_file_organizer_scheduler:latest
```

Run Webserver

```bash
docker run --name video_file_organizer_webserver --env-file ./.env -p 5000:5000 --rm video_file_organizer_webserver:latest
```

Run Scheduler

```bash
docker run --name video_file_organizer_scheduler --env-file ./.env --rm video_file_organizer_scheduler:latest
```
