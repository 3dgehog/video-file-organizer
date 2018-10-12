from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry


def rule_type(fse: FileSystemEntry):
    VALID_OPTIONS = ['season', 'parent-dir', 'sub-dir']
    if fse.rules['type'] not in VALID_OPTIONS:
        fse.valid = False
        return
    pass
