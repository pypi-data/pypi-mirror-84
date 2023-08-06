"""
`mlp.base` module gathers base classes for preprocessors, json config readers
and neural network abstract classes.
"""

from ._base import BasePreprocessor, BaseRNN
from ._base_utils import BaseConfigReader, RNNConfigReader

__all__ = ['BasePreprocessor',
           'BaseRNN',
           'BaseConfigReader',
           'RNNConfigReader']