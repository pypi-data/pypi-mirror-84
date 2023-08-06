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
import datetime
import os
import yaml

from dataframez.catalogs.catalog import Catalog


class Local(Catalog):
    """Local catalog is the abstraction of a catalog in a file-like system."""

    def __init__(self, location: str, name: str, **kwargs):

        # A local catalog will have a path to where the catalog is located and
        self.__location = os.path.expandvars(location)
        self.__name = name
        super().__init__(**kwargs)

    def read(self, entry_name: str, version: int = 0) -> dict:
        """Read in the data catalog entry.

        Args:
            entry_name: Name or key associated with the catalog entry.
            version: Version of the asset being retrieved: default = 0.

        Returns: Catalog entry for the entry name and version.

        """
        self._load_catalog()

        if version == 0:
            version = self.latest_version(entry_name=entry_name)

        entries = self._catalog.get(entry_name)
        entry = [entry for entry in entries['versions'] if entry['number'] == version][0]

        if not entry:
            error_message = f'dataframez: when attempting to read from catalog, {entry_name} did not exist. It is possible that version {version} is not ' \
                            f'there, but {entry_name} is.'
            self._logger.error(error_message)
            raise ValueError(error_message)

        return {
            'type': entries['type'],
            'config': entry['asset_configuration']
        }

    def latest_version(self, entry_name: str) -> int:
        """Retrieve the latest version of a catalog entry.

        Args:
            entry_name: Name of catalog entry.

        Returns: The largest version number.

        """
        if entry_name in self._catalog.keys():
            versions = self._catalog[entry_name]['versions']
            if isinstance(versions, dict):
                return versions['number']
            return max([version['number'] for version in versions])
        return 0

    def register(self, entry_name: str, object_type: str, version: int, asset_configuration: dict) -> None:
        """Register class with catalog. Creates a new entry or adds a version to an existing entry.

        Args:
            entry_name: Name of catalog entry.
            object_type: The kind of entry (data object type) being registered.
            version: Version of the object being registered.
            asset_configuration: Configuration used to save the data to the chosen persistent storage.
        """
        self._load_catalog()

        if self._check_if_registered(entry_name=entry_name):
            self._logger.info('Entry % already exists. Creating a new version of the entry.', entry_name)
            versions = self._catalog[entry_name]['versions']
            if isinstance(versions, dict):
                versions = [versions]
                self._catalog[entry_name]['versions'] = versions
            self._catalog[entry_name]['versions'].append(
                {
                    'number': version,
                    'asset_configuration': asset_configuration,
                    'create_timestamp': datetime.datetime.timestamp(datetime.datetime.utcnow())
                }
            )
        else:
            self._catalog[entry_name] = {
                'type': object_type,
                'versions': [
                    {
                        'number': version,
                        'asset_configuration': asset_configuration,
                        'create_timestamp': datetime.datetime.timestamp(datetime.datetime.utcnow())
                    }
                ]
            }

        self._update_catalog()
        self._load_catalog()

    def validate_entry_type(self, entry_name: str, asset_type: str) -> bool:
        """Validate that the entry is of the correct type. It is possible that someone attempts to create a new data asset of a different data type.

        Args:
            entry_name: Name of asset
            asset_type: Type of persistence being targeted.

        Returns: True if the entry_name and asset_type match in the catalog entry. True also if new entry. False otherwise.

        """
        if self._check_if_registered(entry_name=entry_name):
            return self._catalog.get(entry_name)['type'].lower() == asset_type
        return True

    def list_assets(self) -> list:
        """
        Return a list of all asset names.
        Returns: list of asset names.

        """
        return list(self._catalog.keys())

    def _load_catalog(self) -> None:
        """Read catalog into memory"""
        catalog_path = os.path.join(self.__location, self.__name)

        if not os.path.exists(catalog_path):
            if not os.path.exists(self.__location):
                os.mkdir(self.__location)

            stream = open(catalog_path, 'w')
            stream.close()

        # Read catalog into memory
        with open(catalog_path, 'r') as stream:
            self._catalog = yaml.safe_load(stream)
            if not self._catalog:
                self._catalog = {}

    def _update_catalog(self):
        """Update in-memory catalog."""
        with open(os.path.join(self.__location, self.__name), 'w') as stream:
            _ = yaml.dump(self._catalog, stream)

    def _check_if_registered(self, entry_name: str) -> bool:
        """Check if entry exists in catalog."""
        if self._catalog.get(entry_name):
            return True
        return False
