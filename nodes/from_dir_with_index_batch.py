import os
import torch
import numpy as np
from PIL import Image, ImageOps

"""
    Load an image batch from directory using an index string to get positions: "0,2,5,...n"
"""

class LoadImagesFromDirByIndexBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "indices": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT")
    FUNCTION = "load_images"
    CATEGORY = "northTools"

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
            return (None, None, 0)
        dir_files = os.listdir(directory)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]
        dir_files = sorted(dir_files)
        if not indices.strip():
            raise StopIteration("Waiting for valid indices string.")
        index_list = self._parse_indices(indices, len(dir_files))
        if not index_list:
            raise StopIteration("Waiting for valid indices string.")
        selected_files = [os.path.join(directory, dir_files[i]) for i in index_list]
        images = []
        masks = []
        for path in selected_files:
            i = Image.open(path)
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image_np = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)[None,]
            if 'A' in i.getbands():
                mask_np = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask_tensor = 1. - torch.from_numpy(mask_np)
            else:
                # use image_tensor's height and width
                mask_tensor = torch.zeros((image_tensor.shape[1], image_tensor.shape[2]), dtype=torch.float32)
            images.append(image_tensor)
            masks.append(mask_tensor)
        image_batch = torch.cat(images, dim=0) if images else torch.zeros(0)
        mask_batch = torch.stack(masks, dim=0) if masks else torch.zeros(0)
        return (image_batch, mask_batch, len(images))