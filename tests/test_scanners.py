from video_file_organizer.scanners import scan_input_dir, scan_series_dirs


def test_scan_input_dir(tmp_config_populated):
    scan_input_dir(tmp_config_populated)


def test_scan_series_dirs(tmp_config_populated):
    scan_series_dirs(tmp_config_populated)
