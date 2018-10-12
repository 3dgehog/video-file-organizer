from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry
from video_file_organizer.rules import set_after_match


@set_after_match
def rule_type(fse: FileSystemEntry, *args, **kwargs):
    VALID_OPTIONS = ['season', 'parent-dir', 'sub-dir']
    if not isinstance(fse, FileSystemEntry):
        raise ValueError("Received an argument other than a FileSystemEntry")
    if fse.rules.get('type') not in VALID_OPTIONS:
        fse.valid = False
        return
