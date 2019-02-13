# Video File Oraganiser (DEV)

## Run tests

```bash
pipenv run tests
```

Run tests with log outputs

```bash
pipenv run tests --log-file tests.log
```

## toolbox

A small set of tools used to help develop and test

### mock folder

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