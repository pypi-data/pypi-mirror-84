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

from providah.factories.package_factory import PackageFactory as pf
import pandas as pd
import yaml


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

@pd.api.extensions.register_dataframe_accessor('dataframez')
class CatalogWriter:
    """Extends pandas DataFrame to write to a cataloged persistent storage."""
    __logger = logging.getLogger()
    if platform.lower() != 'windows':
        __configuration_path: str = os.path.join(os.getenv("HOME"), '.dataframez/configuration.yml')
    else:
        __configuration_path: str = os.path.join(os.getenv("USERPROFILE"), '.dataframez/configuration.yml')
    __writers: dict = {}

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.__configure_writer_methods()
        self.__configure_catalog()

    def __configure_catalog(self) -> None:
        """Constructor method that calls factory to create catalog instance."""
        # When a configuration already exists, load it
        with open(self.__configuration_path, 'r') as stream:
            registry_configuration = yaml.safe_load(stream)['configurations']['catalog']

        # Load the configuration
        self.__catalog = pf.create(key=registry_configuration['type'],
                                   configuration=registry_configuration['conf'])

    def __configure_writer_methods(self):
        """Constructor method to populate allowed writer methods"""
        # ----------- create local registry of all writers ---------- #
        # Load configuration
        with open(self.__configuration_path, 'r') as config_stream:
            configuration = yaml.safe_load(stream=config_stream)['configurations']

        for key, value in configuration['writers'].items():
            if value['conf']['allowed']:
                self.__writers[key.lower()] = pf.create(key=value['type'].lower(),
                                                        library='dataframez',
                                                        configuration=value['conf']).write

    def to_csv(self,
               register_as: str,
               sep=',',
               na_rep='',
               float_format=None,
               columns=None,
               header=True,
               index=True,
               index_label=None,
               mode='w',
               encoding=None,
               compression='infer',
               quoting=None,
               quotechar='"',
               line_terminator=None,
               chunksize=None,
               date_format=None,
               doublequote=True,
               escapechar=None,
               decimal='.',
               errors='strict') -> None:
        """
        Write CSV to persistence layer dictated by configuration and asset name.
        Args:
            register_as: Name of asset in catalog.
            sep:
            na_rep:
            float_format:
            columns:
            header:
            index:
            index_label:
            mode:
            encoding:
            compression:
            quoting:
            quotechar:
            line_terminator:
            chunksize:
            date_format:
            doublequote:
            escapechar:
            decimal:
            errors:

        Returns:

        """

        if 'csv' not in self.__writers.keys():
            raise PermissionError('to_csv not supported with the current configuration. Please check your configuration or speak to your system administrator '
                                  'if you believe that this is may be in error.')

        self.__writers['csv'](_df=self._df, entry_name=register_as, **{'sep': sep,
                                                                       'na_rep': na_rep,
                                                                       'float_format': float_format,
                                                                       'columns': columns,
                                                                       'header': header,
                                                                       'index': index,
                                                                       'index_label': index_label,
                                                                       'mode': mode,
                                                                       'encoding': encoding,
                                                                       'compression': compression,
                                                                       'quoting': quoting,
                                                                       'quotechar': quotechar,
                                                                       'line_terminator': line_terminator,
                                                                       'chunksize': chunksize,
                                                                       'date_format': date_format,
                                                                       'doublequote': doublequote,
                                                                       'escapechar': escapechar,
                                                                       'decimal': decimal,
                                                                       'errors': errors})

    def to_pickle(self, register_as: str, compression: str = 'infer', protocol: int = -1) -> None:
        """
        Write Pickle to persistence layer dictated by configuration and asset name.
        Args:
            register_as: Name of asset in catalog.
            compression:
            protocol:

        """
        if 'parquet' not in self.__writers.keys():
            raise PermissionError('to_parquet not supported with the current configuration. Please check your configuration or speak to your system '
                                  'administrator if you believe that this is may be in error.')

        self.__writers['pickle'](_df=self._df, entry_name=register_as, **{'compression': compression,
                                                                          'protocol': protocol})

    def to_parquet(self, register_as: str, engine='auto', compression='snappy', index=None, **kwargs):
        """
        Write Parquet to persistence layer dictated by configuration and asset name.
        Args:
            register_as: Name of asset in catalog.
            engine:
            compression:
            index:
            **kwargs:

        Returns:

        """
        if 'parquet' not in self.__writers.keys():
            raise PermissionError('to_parquet not supported with the current configuration. Please check your configuration or speak to your system '
                                  'administrator if you believe that this is may be in error.')

        self.__writers['parquet'](_df=self._df, entry_name=register_as, **{'compression': compression,
                                                                           'engine': engine,
                                                                           'index': index,
                                                                           **kwargs})
