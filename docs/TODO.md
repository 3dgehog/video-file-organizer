### v3

- [x] Move README TODO to it's own section
- [x] Add all config options as parameters
- [x] Add all config options as environment variables
- [x] Don't give option to create config file
- [x] Add all rulebook options as parameters
- [x] Add all rulebook options as environment variables
- [x] Update logging on the app & add parameter for verbose
- [ ] Updated systemd setup
- [ ] Add warning when file was not found or unsuccessful
- [ ] Stop retrying the same file over and over after failed
- [ ] Sort movies as well
- [ ] Add smart detection using internet (automatic mode)
- [ ] Merge rulebook with config (manual mode)
- [ ] Add a detect format feature (check the output folder contains and guess -> strict)

Remove vfile_consumer, put the operation in the app level
Observee back to an instance instead of class object
notify using name, instead of class name
Vfile attribute to objects, add validation there
update videocollection structure, don't like how its a list of vfiles -> prefer entries (when it comes to deleting or transfering it makes more sense, either the whole thing goes or nothing)
Season rule by default maybe
Add rule per release group (Horriblesubs episode only example)
Similar config to Flexget (think about)
Switch to tasks system instead of using transfer attribute
Pass Entry's not Vfiles
Finished webserver flow
Dockerfile

### v4
Update plugins to use events to register them
Move everything onto one config file
Webserver in thread, not seperated service
