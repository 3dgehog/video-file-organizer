# NOTES

## TODO

- [x] Add a lock file to prevent two instances
- [x] Setup logging
- [x] Replace if episode already exists in folder (no-replace)
- [x] Create systemd service and timer (instead of cron)
- [] check if a later episode exists and send a warning message for it (incase a new season from a untraditional season show appears)
- [x] Switch to pipenv
- [x] Fix logging so that warning & critical are only used for breaking scenerios and not rule failer. Also only use info for things on the systemd logger.
- [x] ~~make systemd service/timer that uses the environment in `/etc/profile.d` to find working directory and link it strait with `systemctl link` (updatable)~~ Working directory need to be static, toolbox generates systemd files now
- [x] Add a log on file that records only relavant debug information for all transactions (for traceback incase somefile went horribly wrong in the past)
- [x] Add --config -c to define config location
- [x] By default vfo should create a new Season folder if it doesn't exist
- [x] no-replace rule doesn't delete the file after it was check successfully
- [] create before_script.d directory to link before scripts strait into the app without needed to add them to the config file
- [x] Remove traceback on before_script failing
- [] Rework the logs, more information about the files for the vfo.logs
- [x] Issue when episode number isn't detected
- [] Fix empty series folder error

## Notes to self
