"""
ComfyUI-northTools Extension

This module provides additional tools and utilities for ComfyUI.
Author: Northumber (Teo Toscano)
"""

from .nodes.from_dir_image_list import LoadImagesFromDirList
from .nodes.extract_metadata_by_key import ExtractMetadataByKey
from .nodes.sum_integers import SumIntegers


NODE_CLASS_MAPPINGS = {
  "LoadImagesFromDirList": LoadImagesFromDirList,
  "ExtractMetadataByKey": ExtractMetadataByKey,
  "SumIntegers": SumIntegers,
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "LoadImagesFromDirList": "Load Image List from Directory",
  "ExtractMetadataByKey": "Extract Metadata value by key",
  "SumIntegers": "Sum Integers",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
