from tests.vars import VFILES_IN_ASSETS

from video_file_organizer.models import VideoFile
from video_file_organizer.matchers import MetadataMatcher


def test_metadatamatcher():
    metadata_matcher = MetadataMatcher()

    # Only take assets with metadata key
    metadata_assets = [x for x in VFILES_IN_ASSETS if x.get('metadata')]
    vfiles = [VideoFile(name=x['name']) for x in metadata_assets]

    for vfile in vfiles:
        metadata_matcher.by_vfile(vfile=vfile)
        for item in metadata_assets:
            if item['name'] == vfile.name:
                for key, value in item['metadata'].items():
                    # Test metadata added successfully to vfile
                    assert vfile.metadata[key] == value
