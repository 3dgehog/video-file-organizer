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

### SystemD

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