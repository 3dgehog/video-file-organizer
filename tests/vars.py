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
    "That 70s Show": 'season',
    "Re Zero kara Hajimeru Isekai Seikatsu": 'parent-dir',

    "Akudama Drive": "parent-dir",
    "Haikyuu!! To the Top 2nd Season": 'sub-dir "Season 5"',
    "Jujutsu Kaisen": "parent-dir",
    "Kamisama ni Natta Hi": "parent-dir",
    "Maoujou de Oyasumi": "parent-dir",
    "Munou na Nana": "parent-dir",
    "Shingeki no kyojin": 'sub-dir "Season 4"'
}

SERIES_PARMS = [
    "--series-rule", "Boruto - Naruto Next Generations", "parent-dir", "episode-only", "alt-title",
    "--series-rule", "Gintama", "parent-dir", "episode-only",
    "--series-rule", "One Punch Man", "season",
    "--series-rule", "Mahoutsukai no Yume", "parent-dir",
    "--series-rule", "One Piece", "sub-dir", "One Piece Episodes", "episode-only", "format-title", "One_Piece_{{ episode }}",
    "--series-rule", "American Dad", "season",
    "--series-rule", "Arrow", "season",
    "--series-rule", "Brooklyn Nine Nine", "season",
    "--series-rule", "Fresh off the Boat", "season",
    "--series-rule", "Homeland", "season",
    "--series-rule", "Lucifer", "season",
    "--series-rule", "Marvels Agents of S.H.I.E.L.D", "season",
    "--series-rule", "Supernatural", "season",
    "--series-rule", "The Big Bang Theory", "season",
    "--series-rule", "The Flash", "season",
    "--series-rule", "Vikings", "season",
    "--series-rule", "That 70s Show", "season",
    "--series-rule", "Re Zero kara Hajimeru Isekai Seikatsu", "parent-dir",

    "--series-rule", "Akudama Drive", "parent-dir",
    "--series-rule", "Haikyuu!! To the Top 2nd Season", 'sub-dir', "Season 5",
    "--series-rule", "Jujutsu Kaisen", "parent-dir",
    "--series-rule", "Kamisama ni Natta Hi", "parent-dir",
    "--series-rule", "Maoujou de Oyasumi", "parent-dir",
    "--series-rule", "Munou na Nana", "parent-dir",
    "--series-rule", "Shingeki no kyojin", 'sub-dir', "Season 4"
]
