# Modifications © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
from sys import platform

import pandas as pd
import yaml
from providah.factories.package_factory import PackageFactory as pf

from dataframez.catalogs.catalog import Catalog


class __CatalogReader:
    """Class to help manage and hide reading data from the data catalog."""
    # Catalog abstraction instance
    __catalog: Catalog
    # True once initialized (configured)
    __initialized = False
    # Reader methods that have been allowed
    __readers: dict = {}
    # Application logger instance
    __logger = logging.getLogger()
    # Path to configuration file.
    if platform.lower() != 'windows':
        __configuration_path: str = os.path.join(os.getenv("HOME"), '.dataframez/configuration.yml')
    else:
        __configuration_path: str = os.path.join(os.getenv("USERPROFILE"), '.dataframez/configuration.yml')
    @classmethod
    def __initialize(cls):

        if not cls.__initialized:
            cls.__configure_catalog()
            cls.__configure_reader_methods()
        cls.__initialized = True

    @classmethod
    def read(cls, entry_name: str, version: int = 0, **kwargs) -> pd.DataFrame:
        """
        Read from data catalog given the data asset catalog name and the version.
        Args:
            entry_name: Name of data catalog entry
            version: Version of data asset
            **kwargs:

        Returns:

        """
        cls.__initialize()
        asset_info = cls.__catalog.read(entry_name=entry_name,
                                        version=version)

        return cls.__readers[asset_info['type']](asset_info,
                                                 **kwargs)

    @classmethod
    def __configure_catalog(cls) -> None:
        """Constructor method that calls factory to create catalog instance."""
        # When a configuration already exists, load it
        with open(cls.__configuration_path, 'r') as stream:
            registry_configuration = yaml.safe_load(stream)['configurations']['catalog']

        # Load the configuration
        cls.__catalog = pf.create(key=registry_configuration['type'],
                                  configuration=registry_configuration['conf'])

    @classmethod
    def __configure_reader_methods(cls):
        """Constructor method to populate allowed reader methods"""
        # ----------- create local registry of all writers ---------- #
        # Load configuration
        with open(cls.__configuration_path, 'r') as config_stream:
            configuration = yaml.safe_load(stream=config_stream)['configurations']

        for key, value in configuration['writers'].items():
            if value['conf']['allowed']:
                cls.__readers[key.lower()] = pf.create(key=value['type'].lower(),
                                                       library='dataframez',
                                                       configuration=value['conf']).read

    @classmethod
    def list_assets(cls) -> list:
        return cls.__catalog.get_assets()


def __read_from_catalog(entry_name: str, version: int = 0) -> pd.DataFrame:

    return __CatalogReader.read(entry_name=entry_name, version=version)
