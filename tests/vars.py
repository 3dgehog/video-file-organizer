# flake8: noqa

import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

SERIES_CONFIGPARSE = {
    "Boruto - Naruto Next Generations": 'parent-dir episode-only alt-title',
    "Gintama": 'parent-dir episode-only',
    "One Punch Man": 'season',
    "Mahoutsukai no Yome": 'parent-dir',
    "One Piece": 'sub-dir "One Piece Episodes" episode-only \
format-title "One_Piece_{{ episode }}"',
    "American Dad": 'season',
    "Arrow": 'season',
    "Brooklyn Nine Nine": 'season',
    "Fresh off the Boat": 'season',
    "Homeland": 'season',
    "Lucifer": 'season',
    "Marvels Agents of S.H.I.E.L.D": 'season',
    "Supernatural": 'season',
    "The Big Bang Theory": 'season',
    "The Flash": 'season',
    "Vikings": 'season',
    "That 70s Show": 'season'
}


VFILES_IN_ASSETS = [
    {
        'name': 'The.Flash.2014.S04E16.HDTV.x264-SVA.mkv',
        'metadata': {
            'title': 'The Flash',
            'year': 2014,
            'season': 4,
            'episode': 16,
            'source': 'HDTV',
            'video_codec': 'H.264',
            'release_group': 'SVA',
            'container': 'mkv',
            'mimetype': 'video/x-matroska',
            'type': 'episode'}
    },
    {
        'name': 'Brooklyn.Nine-Nine.S05E13.HDTV.x264-SVA.mkv'
    },
    {
        'name': 'Arrow.S06E10.PROPER.HDTV.x264-CRAVERS.mkv'
    },
    {
        'name': 'The.Big.Bang.Theory.S11E17.HDTV.x264-KILLERS.mkv'
    },
    {
        'name': 'Homeland.S07E06.WEB.H264-DEFLATE.mkv'
    },
    {
        'name': '[HorribleSubs] Mahoutsukai no Yome - 24 [480p].mkv'
    },
    {
        'name': '[HorribleSubs] One Piece - 829 [720p].mkv'
    },
    {
        'name': 'lucifer.s03e06.web.PROPER.x264-tbs.mkv'
    },
    {
        'name': 'Lucifer.S03E13.PROPER.WEBRip.x264-ION10.mp4'
    },
    {
        'name': 'The.Flash.2014.S04E16.PROPER.HDTV.x264-CRAVERS.mkv',
        'metadata': {
            'title': 'The Flash',
            'type': 'episode'
        }
    },
    {
        'name': '[HorribleSubs] Gintama - 353 [480p].mkv',
        'metadata': {
            'release_group': 'HorribleSubs',
            'title': 'Gintama',
            'episode': 353,
            'screen_size': '480p',
            'container': 'mkv',
            'mimetype': 'video/x-matroska',
            'type': 'episode'
        }
    },
    {
        'name': 'American.Dad.S15E06.WEBRip.x264-ION10.mp4'
    },
    {
        'name': 'Marvels.Agents.of.S.H.I.E.L.D.S05E14.HDTV.x264-SVA.mkv'
    },
    {
        'name': 'Fresh.Off.the.Boat.S04E14.WEBRip.x264-ION10.mp4'
    },
    {
        'name': 'Marvels.Agents.of.S.H.I.E.L.D.S05E14.PROPER.WEBRip.x264-ION10.mp4'
    },
    {
        'name': '[HorribleSubs] Boruto - Naruto Next Generations - 50 [480p].mkv'
    },
    {
        'name': 'Vikings.S05E10.HDTV.x264-KILLERS.mkv'
    },
    {
        'name': 'Supernatural.S13E15.HDTV.x264-KILLERS.mkv'
    },
    {
        'name': '[HorribleSubs] One Punch Man S2 - 03 [480p].mkv'
    },
    {
        'name': 'The.Flash.2014.S04E11.REPACK.HDTV.x264-SVA.mkv'
    }
]
