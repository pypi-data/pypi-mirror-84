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


class Catalog:
    """Base class for all Catalog types. Catalog types are abstractions that abstract the interactions with a 'data catalog.'"""

    # instance of python logger
    _logger = logging.getLogger()

    # catalog is stored - in memory (at this time) - as a dictionary
    _catalog: dict

    def __init__(self, **kwargs):
        # pylint: disable=unused-argument
        # Regardless of class, the in-memory component must be loaded.
        self._load_catalog()

    def read(self, entry_name: str, version: int = 1) -> dict:
        raise NotImplementedError()

    def register(self, entry_name: str, object_type: str, version: int, asset_configuration: dict) -> None:
        raise NotImplementedError()

    def validate_entry_type(self, entry_name: str, asset_type: str) -> bool:
        raise NotImplementedError()

    def latest_version(self, entry_name: str) -> int:
        raise NotImplementedError()

    def list_assets(self) -> list:
        raise NotImplementedError()

    # ----------- Protected Methods Below ------------- #

    def _check_if_registered(self, entry_name: str) -> bool:
        raise NotImplementedError()

    def _load_catalog(self) -> None:
        raise NotImplementedError()

    def _update_catalog(self):
        raise NotImplementedError()
