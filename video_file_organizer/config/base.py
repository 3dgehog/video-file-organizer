import abc
import os

from typing import Optional, List, Union


class ConfigBase(metaclass=abc.ABCMeta):
    custom_path: Optional[str] = None
    default_filename: Optional[str] = None
    default_path: Optional[str] = None
    args: List[str]

    def load_args(self, args, **kwargs) -> list:
        return args

    def load_env(self, env, **kwargs) -> list:
        return [env]

    @abc.abstractmethod
    def load_file(self, path: str, **kwargs) -> dict:
        pass

    def search_config(
            self,
            name: str,
            required: bool = False,
            in_args: bool = True,
            in_env: bool = True,
            in_file: bool = True,
            **kwargs
    ) -> Union[list, None]:
        """Searches for config in 5 different locations: args, env,
        the current directory, a custom path & the default path

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
        if in_args and self.args:
            if name in self.args:
                args = self.load_args(self.args, name=name, **kwargs)
                if getattr(args, kwargs.get('arg_name') or name):
                    return getattr(args, kwargs.get('arg_name') or name)

        # environment
        # returns a list and changes it to strings
        if in_env:
            if os.environ.get(kwargs.get('env_name') or name.upper()):
                return self.load_env(
                    os.environ.get(
                        kwargs.get('env_name') or name.upper()
                    ), **kwargs
                )

        # current directory
        if in_file:
            if self.default_filename:
                if os.path.exists(self.default_filename):
                    file = self.load_file(self.default_filename)
                    if file.get(kwargs.get('file_name') or name):
                        return file.get(kwargs.get('file_name') or name)

        # custom file location
        if in_file:
            if self.custom_path:
                file = self.load_file(self.custom_path, name=name, **kwargs)
                if file.get(kwargs.get('file_name') or name):
                    return file.get(kwargs.get('file_name') or name)

        # default file locations
        if in_file:
            if self.default_path:
                if os.path.exists(self.default_path):
                    file = self.load_file(self.default_path)
                    if file.get(kwargs.get('file_name') or name):
                        return file.get(kwargs.get('file_name') or name)

        if required:
            raise ValueError(
                f"Couldn't find required config for {name.capitalize()}")
        return None
