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
from sys import platform

import yaml
from dataframez.read_from_catalog import __read_from_catalog
import os
import pandas as pd
import providah.factories.package_factory as pf

# Fill class registry
pf.PackageFactory.fill_registry()

# Create configuration
config_path = os.path.join(os.getenv("HOME"), ".dataframez/configuration.yml")

# Set the path to the default configuration
if platform.lower() != 'windows':
    default_config_path: str = os.path.join(os.path.dirname(__file__), 'configurations/default_configuration.yml')
else:
    default_config_path: str = os.path.join(os.path.dirname(__file__), 'configurations/default_configuration_windows.yml')

#  If the configuration path does not exist - then a default configuration will be created
if not os.path.exists(config_path):

    # Set the path for the default configuration if it does not exist
    catalog_location = os.path.join(os.getenv("HOME"), ".dataframez")
    if not os.path.exists(catalog_location):
        os.mkdir(catalog_location)

    # Load the default configuration
    with open(default_config_path, 'r') as default_stream:
        registry_configuration = yaml.safe_load(default_stream)

    # Write the default configuration
    with open(config_path, 'w') as stream:
        _ = yaml.dump(registry_configuration, stream)


# Add ability to read from pandas
pd.from_catalog = __read_from_catalog
