import abc
import os

from typing import Optional, List, Union


class ConfigBase(metaclass=abc.ABCMeta):
    custom_path: Optional[str] = None
    default_filename: Optional[str] = None
    default_path: Optional[str] = None
    args: List[str]

    def load_args(self, args, **kwargs):
        return args

    def load_env(self, env, **kwargs):
        return env.split(':')

    @abc.abstractmethod
    def load_file(self, path: str, **kwargs) -> dict:
        pass

    def search_config(self, name: str, required: bool = False,
                      **kwargs) -> Union[list, None]:
        """Searches for config in 4 different places, args, env,
        a custom location & default location

        Args:
            name (str): The name of the config
            required (bool, optional): If this config is required. Defaults to
                False.

        Keyword Arguments:
            arg_name (str): Overwrites the default name for arguments
            env_name (str): Overwrites the default name for env variables
            file_name (str): Overwrites the default name for files

        Raises:
            ValueError: When the config couldn't be found and required is true

        Returns:
            list: It returns everything as a list
        """
        # args
        # returns list but doesn't change to string
        if name in self.args:
            args = self.load_args(self.args, name=name, **kwargs)
            if getattr(args, kwargs.get('arg_name') or name):
                return getattr(args, kwargs.get('arg_name') or name)

        # environment
        # returns a list and changes it to strings
        if os.environ.get(kwargs.get('env_name') or name.upper()):
            env = self.load_env(os.environ.get(
                kwargs.get('env_name') or name.upper(), **kwargs
            ))
            return env

        # custom file location
        if self.custom_path:
            file = self.load_file(self.custom_path, name=name, **kwargs)
            if file.get(kwargs.get('file_name') or name):
                return file.get(kwargs.get('file_name') or name)

        # default file locations
        if self.default_path:
            if os.path.exists(self.default_path):
                file = self.load_file(self.default_path)
                if file.get(kwargs.get('file_name') or name):
                    return file.get(kwargs.get('file_name') or name)

        # current directory
        if self.default_filename:
            if os.path.exists(self.default_filename):
                file = self.load_file(self.default_filename)
                if file.get(kwargs.get('file_name') or name):
                    return file.get(kwargs.get('file_name') or name)

        if required:
            raise ValueError(
                f"Couldn't find required config for {name.capitalize()}")
        return None
