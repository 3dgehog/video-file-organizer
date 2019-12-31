import os
import re
import logging
import jinja2

from typing import Union

logger = logging.getLogger('app.series.rules')

# after match


def rule_season(
        name: str,
        guessit: dict,
        match: dict,
        transfer: dict = {}) -> Union[dict, None]:
    """Sets transfer_to to the correct season folder

    Args:
        name (str): Name of the file
        guessit (dict): guessit dictionary of the file
        match (dict): match dictionary of the file
        transfer (dict, optional): tranfer dictionary of the file. 
            Defaults to {}.

    Returns:
        dict: transfer dictionary with new 'transfer_to' key & value
    """
    logger.debug(f"Applying rule 'season' to {name}")

    if 'season' not in guessit:
        logger.warn("Rule 'season' FAILED: ",
                    f"Undefined season number for file: {name}")
        return None

    season = str(guessit['season'])
    for sub_name, sub_entry in match['sub_entries'].items():
        search = re.search(f"^Season {season}", sub_name, re.IGNORECASE)
        if search:
            transfer['transfer_to'] = sub_entry['_entry'].path

    if 'transfer_to' not in transfer:
        path_to_new_season_dir = os.path.join(
            match['_entry'].path, f"Season {season}")
        # os.mkdir(path_to_new_season_dir)
        print(f"NEW DIRECTORY CREATED {path_to_new_season_dir}")
        transfer['transfer_to'] = path_to_new_season_dir
        logger.info("Rule 'season' " +
                    f"Created new Season {season} folder for Series {name}")

    logger.debug(f"Rule 'season' OK for {name}")
    return transfer


def rule_parent_dir(name: str, match: dict, transfer: dict = {}) -> dict:
    """Sets 'trasnfer_to to the parent directory

    Args:
        name (str): Name of the file
        match (dict): match dictionary of the file
        transfer (dict, optional): transfer dictionary of the file.
            Defaults to {}.

    Returns:
        dict: transfer dictionary with new 'transfer_to' key & value
    """
    logger.debug(f"Applying rule 'parent-dir' to {name}")
    transfer['transfer_to'] = match['_entry'].path

    logger.debug(f"Rule 'parent-dir' OK for {name}")
    return transfer


def rule_sub_dir(
        name: str, match: dict, rules: list, transfer: dict = {}) -> dict:
    """Sets the transfer_to a specified sub directory

    Args:
        name (str): Name of the file
        match (dict): match dictionary of the file
        rules (list): rules list of the file
        transfer (dict, optional): transfer dictionary of the file.
            Defaults to {}.

    Returns:
        dict: transfer dictionary with new 'transfer_to' key & value
    """
    logger.debug(f"Applying rule 'sub-dir' to {name}")
    subdir_name_index = rules.index('sub-dir') + 1
    subdir_name = rules[subdir_name_index]
    if subdir_name not in match['sub_entries'].keys():
        logger.warn("Rule 'sub-dir' FAILED: " +
                    f"Cannot locate sub-dir {subdir_name}: {name}")
        return transfer

    transfer['transfer_to'] = match['sub_entries'][subdir_name]['_entry'].path

    logger.debug(f"Rule 'sub-dir' OK for {name}")
    return transfer


def rule_episode_only(name: str, guessit: dict) -> dict:
    """Removes guessit['season'] and merges it with guessit['episode']"""
    logger.debug(f"Applying rule 'episode-only' to {name}")
    try:
        guessit['episode'] = int(
            str(guessit['season']) + str(guessit['episode']))
    except KeyError:
        # Any episode number below 100 will raise... therefore its ignored
        pass
    guessit.copy().pop('season', None)

    logger.debug(f"Rule 'episode-only' OK for {name}")
    return guessit


def rule_format_title(
        name: str, guessit: dict, rules: list, transfer: dict) -> dict:
    """Sets transfer_to filename to a specified name for transfer"""
    logger.debug(f"Applying rule 'format-title' to {name}")
    if not guessit.get('container') or not transfer['transfer_to']:
        logger.warn("Rule 'format-title' FAILED: " +
                    f"Missing container or transfer_to value: {name}")
        return transfer

    format_index = rules.index('format-title') + 1
    template = jinja2.Template(
        str(rules[format_index]) + "." + str(guessit['container']))
    new_name = template.render(guessit)
    transfer['transfer_to'] = os.path.join(transfer['transfer_to'], new_name)

    logger.debug(f"Rule 'format-title' OK for {name}")
    return transfer


def rule_alt_title(name: str, guessit: dict) -> dict:
    """Checks if the fse has an alternative title and merges it with the
    current title"""
    logger.debug(f"Applying rule 'alternative_title' to {name}")
    if 'alternative_title' not in guessit:
        logger.warn("Rule 'alternative_title' FAILED: " +
                    f"Alternative title missing: {name}")
        return guessit
    guessit['title'] = ' '.join([
        guessit['title'], guessit['alternative_title']
    ])

    logger.debug(f"Rule 'alternative_title' OK for {name}")
    return guessit
