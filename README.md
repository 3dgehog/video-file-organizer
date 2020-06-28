# Video File Organizer

## Installation

### Get source files and install

Clone the directory with git then:

```bash
cd video_file_organizer
pipenv install
```

### Setting up config files

Before automizing the program, the setup config and rule book need to be setup. Run the program once to get empty config files created in `~/.config/video_file_orgainzer`

```bash
pipenv run vfo
```

### Setup systemd service and timer

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

## Development

### Run tests

```bash
pipenv run tests
```

Run tests with log outputs

```bash
pipenv run tests --log-file tests.log
```

### toolbox

A small set of tools used to help develop and test

#### mock folder

You can use the toolbox to create a full mock folder of blank folders to test against. The mock folder will also have setup the most basic configs to start your tests. To use:

```bash
pipenv run python toolbox.py --mock
```

Then run the software against that folder by precizing the configs folder location

```bash
pipenv run vfo -c mock/configs
```

#### Testing systemd with mock files

Generate the systemd files with the toolbox

```bash
pipenv run python toolbox.py --systemd
```

Then edit `vfo.service` and append `-c mock/configs` to the end of ExecStart to run systemd against the mock files

```text
ExecStart = /usr/local/bin/pipenv run vfo -c mock/configs
```

## Todos

- [x] Send single file name through http to process
  - [] Add warning when file was not found or unsuccessful
- [] merge video-file-renamer into this project to be able to detect what kind of video file it is (replace rulebook)
- [] Sort movies as well
- [] Stop retrying the same file over and over after failed
