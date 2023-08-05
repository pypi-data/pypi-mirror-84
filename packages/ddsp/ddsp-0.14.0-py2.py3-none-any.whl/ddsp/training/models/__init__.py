# Copyright 2020 The DDSP Authors.
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

# Lint as: python3
"""Module with all the global configurable models for training."""

from ddsp.training.models.autoencoder import Autoencoder
from ddsp.training.models.model import Model
from ddsp.training.models.transcribing_autoencoder import TranscribingAutoencoder
import gin

_configurable = lambda cls: gin.configurable(cls, module=__name__)

Autoencoder = _configurable(Autoencoder)
TranscribingAutoencoder = _configurable(TranscribingAutoencoder)


@gin.configurable
def get_model(model=gin.REQUIRED):
  """Gin configurable function get a 'global' model for use in ddsp_run.py.

  Convenience for using the same model in train(), evaluate(), and sample().
  Args:
    model: An instantiated model, such as 'models.Autoencoder()'.

  Returns:
    The 'global' model specifieed in the gin config.
  """
  return model
