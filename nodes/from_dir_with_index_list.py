import os
import torch
import numpy as np
from PIL import Image, ImageOps

"""
    Load an image list from directory using an index string to get positions: "0,2,5,...n"
"""

class LoadImagesFromDirByIndexList:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "indices": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "INT")
    RETURN_NAMES = ("IMAGE", "MASK", "FILE PATH", "METADATA", "INDEX COUNT")
    OUTPUT_IS_LIST = (True, True, True, True, True)
    FUNCTION = "load_images"
    CATEGORY = "image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return hash(frozenset(kwargs.items()))

    def _parse_indices(self, indices_str, max_len):
        indices = []
        for idx in indices_str.split(","):
            idx = idx.strip()
            if idx.isdigit():
                i = int(idx)
                if 0 <= i < max_len:
                    indices.append(i)
        return sorted(set(indices))

    def load_images(self, directory: str, indices: str = ""):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")

        dir_files = os.listdir(directory)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]
        dir_files = sorted(dir_files)
        if not dir_files:
            raise FileNotFoundError(f"No valid image files in directory '{directory}'.")

        if not indices.strip():
            raise StopIteration("Waiting for valid indices string.")

        index_list = self._parse_indices(indices, len(dir_files))
        if not index_list:
            raise StopIteration("Waiting for valid indices string.")

        images = []
        masks = []
        file_paths = []
        metadatas = []
        indexes = []

        for idx in index_list:
            image_path = os.path.join(directory, dir_files[idx])
            i = Image.open(image_path)
            i = ImageOps.exif_transpose(i)
            metadata = i.info.copy()
            exif = i.getexif()
            if exif:
                metadata['exif'] = dict(exif)
            metadatas.append(str(metadata))

            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((image.shape[2], image.shape[3]), dtype=torch.float32)

            images.append(image)
            masks.append(mask)
            file_paths.append(str(image_path))
            indexes.append(idx)

        return (images, masks, file_paths, metadatas, indexes)