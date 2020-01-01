import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")

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

VFILE_NAME_LIST = [
    'Marvels.Agents.of.S.H.I.E.L.D.S05E14.HDTV.x264-SVA.mkv',
    '[HorribleSubs] Boruto - Naruto Next Generations - 50 [480p].mkv',
    '[HorribleSubs] Gintama - 353 [480p].mkv',
    '[HorribleSubs] Mahoutsukai no Yome - 24 [480p].mkv',
    '[HorribleSubs] One Piece - 829 [720p].mkv',
    '[HorribleSubs] One Punch Man S2 - 03 [480p].mkv',
    'lucifer.s03e06.web.PROPER.x264-tbs.mkv'
]
