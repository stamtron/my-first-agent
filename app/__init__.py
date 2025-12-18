# Copyright 2025 Google LLC
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

import importlib
import os
import sys

# Default to the main agent if not specified
module_name = os.getenv("ROOT_AGENT_MODULE", "app.agent")

try:
    module = importlib.import_module(module_name)
    app = module.app
except ImportError as e:
    raise ImportError(f"Could not load agent module '{module_name}'. Please check ROOT_AGENT_MODULE env var. Error: {e}")
except AttributeError:
    raise AttributeError(f"Module '{module_name}' must define an 'app' object.")

__all__ = ["app"]
