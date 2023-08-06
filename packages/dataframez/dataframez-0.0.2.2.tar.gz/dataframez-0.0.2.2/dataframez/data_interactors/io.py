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
import pandas as pd
import os
import yaml
from sys import platform
from providah.factories.package_factory import PackageFactory as pf

from dataframez.catalogs.catalog import Catalog


# pylint: disable=too-many-arguments

class IO:
    """Base class for IO operations for data persistence."""
    _logger = logging.getLogger()
    if platform.lower() != 'windows':
        __configuration_path: str = os.path.join(os.getenv("HOME"), '.dataframez/configuration.yml')
    else:
        __configuration_path: str = os.path.join(os.getenv("USERPROFILE"), '.dataframez/configuration.yml')

    def __init__(self, **kwargs):
        # pylint: disable=unused-argument
        with open(self.__configuration_path, 'r') as stream:
            configuration = yaml.safe_load(stream)['configurations']['catalog']
        self._catalog: Catalog = pf.create(key=configuration['type'],
                                           configuration=configuration['conf'])

    def read(self, asset_info: dict, **kwargs) -> pd.DataFrame:
        raise NotImplementedError()

    def write(self, _df: pd.DataFrame, entry_name: str, **kwargs):
        raise NotImplementedError()
