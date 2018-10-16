from tests.utils.injectors import setup_app_with_injectors

from tests.fixtures.setup_assets import SERIES_CONFIGPARSE


def test_success_transferer(
        tmp_config_dir,
        extract_input_dir,
        extract_series_dirs,):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })
    app.setup()
    app.run()
