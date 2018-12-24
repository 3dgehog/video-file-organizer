import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")

SERIES_CONFIGPARSE = {
    "Boruto - Naruto Next Generations": 'parent-dir episode-only alt-title',
    "Gintama": 'parent-dir episode-only',
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