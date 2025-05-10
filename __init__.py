"""
ComfyUI-northTools Extension

This module provides additional tools and utilities for ComfyUI.
Author: Northumber (Teo Toscano)
"""

from .nodes.from_dir_image_list import LoadImagesFromDirList
from .nodes.extract_metadata_by_key import ExtractMetadataByKey
from .nodes.sum_integers import SumIntegers
from .nodes.from_dir_with_index_batch import LoadImagesFromDirByIndexBatch
from .nodes.from_dir_with_index_list import LoadImagesFromDirByIndexList
from .nodes.boolean_list_to_indexes import BooleanIndexesToString
from .nodes.concat_history_string import ConcatHistoryString
from .nodes.image_to_true import ImageToTrue


NODE_CLASS_MAPPINGS = {
  "LoadImagesFromDirList": LoadImagesFromDirList,
  "ExtractMetadataByKey": ExtractMetadataByKey,
  "SumIntegers": SumIntegers,
  "LoadImagesFromDirByIndexBatch": LoadImagesFromDirByIndexBatch,
  "LoadImagesFromDirByIndexList": LoadImagesFromDirByIndexList,
  "BooleanIndexesToString": BooleanIndexesToString,
  "ConcatHistoryString": ConcatHistoryString,
  "ImageToTrue": ImageToTrue,
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "LoadImagesFromDirList": "Load Image List from Directory",
  "ExtractMetadataByKey": "Extract Metadata value by key",
  "SumIntegers": "Sum Integers",
  "LoadImagesFromDirByIndexBatch": "Load Image batch from Directory with indexes",
  "LoadImagesFromDirByIndexList": "Load Image list from Directory with indexes",
  "BooleanIndexesToString": "Boolean list to index string",
  "ConcatHistoryString": "Concatenate and remember string",
  "ImageToTrue": "Image to True",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
