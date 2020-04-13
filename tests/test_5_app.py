# import os

# from video_file_organizer.app import App

# from tests.utils import ConfigFileInjector


# def test_app_setup(tmp_dir):
#     app = App()

#     # Build config file
#     config_injector = ConfigFileInjector(tmp_dir)
#     os.mkdir(os.path.join(tmp_dir, "series_dirs"))
#     os.mkdir(os.path.join(tmp_dir, "input_dir"))
#     config_injector.append({
#         "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
#         "input_dir": os.path.join(tmp_dir, "input_dir")
#     })

#     app.setup(tmp_dir, create=False)
