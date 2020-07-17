import os

from .utils import ConfigFileInjector, RuleBookFileInjector
from .vars import SERIES_CONFIGPARSE

from video_file_organizer.app import App

VFILE_FINAL_PATHS = [
    "anime_dir/One-Punch Man/Season 2/"
    "[HorribleSubs] One Punch Man S2 - 03 [480p].mkv",
    "series_dir/The Flash/Season 4/"
    "The.Flash.2014.S04E11.REPACK.HDTV.x264-SVA.mkv",
    "series_dir/Supernatural/Season 13/"
    "Supernatural.S13E15.HDTV.x264-KILLERS.mkv",
    "series_dir/Vikings/Season 5/"
    "Vikings.S05E10.HDTV.x264-KILLERS.mkv",
    "anime_dir/Boruto - Naruto Next Generations/"
    "[HorribleSubs] Boruto - Naruto Next Generations - 50 [480p].mkv",
    "series_dir/Marvel's Agents of Sheild/Season 5/"
    "Marvels.Agents.of.S.H.I.E.L.D.S05E14.PROPER.WEBRip.x264-ION10.mp4",
    "series_dir/Fresh Off The Boat/Season 4/"
    "Fresh.Off.the.Boat.S04E14.WEBRip.x264-ION10.mp4",
    "series_dir/Marvel's Agents of Sheild/Season 5/"
    "Marvels.Agents.of.S.H.I.E.L.D.S05E14.HDTV.x264-SVA.mkv",
    "series_dir/American Dad/Season 15/"
    "American.Dad.S15E06.WEBRip.x264-ION10.mp4",
    "anime_dir/Gintama/"
    "[HorribleSubs] Gintama - 353 [480p].mkv",
    "series_dir/The Flash/Season 4/"
    "The.Flash.2014.S04E16.PROPER.HDTV.x264-CRAVERS.mkv",
    "series_dir/Lucifer/Season 3/"
    "Lucifer.S03E13.PROPER.WEBRip.x264-ION10.mp4",
    "series_dir/Lucifer/Season 3/"
    "lucifer.s03e06.web.PROPER.x264-tbs.mkv",
    "anime_dir/One Piece/One Piece Episodes/"
    "One_Piece_829.mkv",
    "anime_dir/Mahoutsukai no Yome/"
    "[HorribleSubs] Mahoutsukai no Yome - 24 [480p].mkv",
    "series_dir/Homeland/Season 7/"
    "Homeland.S07E06.WEB.H264-DEFLATE.mkv",
    "series_dir/The Big Bang Theory/Season 11/"
    "The.Big.Bang.Theory.S11E17.HDTV.x264-KILLERS.mkv",
    "series_dir/Arrow/Season 6/"
    "Arrow.S06E10.PROPER.HDTV.x264-CRAVERS.mkv",
    "series_dir/Brooklyn 99/Season 5/"
    "Brooklyn.Nine-Nine.S05E13.HDTV.x264-SVA.mkv",
    "series_dir/The Flash/Season 4/"
    "The.Flash.2014.S04E16.HDTV.x264-SVA.mkv",
    "anime_dir/Re Zero kara Hajimeru Isekai Seikatsu/"
    "[HorribleSubs] Re Zero kara Hajimeru Isekai Seikatsu - 27 [720p].mkv"
]


def test_app(tmp_dir, sample_input_dir, sample_series_dirs):
    config_injector = ConfigFileInjector(tmp_dir)
    config_injector.update({
        "series_dirs": sample_series_dirs,
        "input_dir": sample_input_dir
    })

    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.update('series', SERIES_CONFIGPARSE)

    app = App()
    app.setup(tmp_dir)
    app.run()

    series_folder = os.path.dirname(sample_series_dirs[0])
    for path in VFILE_FINAL_PATHS:
        assert os.path.exists(os.path.join(series_folder, path))
