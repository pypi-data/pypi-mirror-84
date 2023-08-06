"""
`dsg.base` module gathers base classes for preprocessors, json config readers
and neural network abstract classes.
"""

from ._base import BasePreprocessor, BaseRNN

__all__ = ['BasePreprocessor',
           'BaseRNN']