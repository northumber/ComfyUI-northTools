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
                "indices": ("STRING", {"default": ""}),
            },
        }


    RETURN_TYPES = ("IMAGE", "MASK", "INT")
    FUNCTION = "load_images"


    CATEGORY = "image"


    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return hash(frozenset(kwargs.items()))


    def _parse_indices(self, indices_str, max_len):
        # Parse a string like "0,3,4" into unique, sorted, safe integer indexes within [0,max_len-1]
        indices = []
        for idx in indices_str.split(","):
            idx = idx.strip()
            if idx.isdigit():
                i = int(idx)
                if 0 <= i < max_len:
                    indices.append(i)
        return sorted(set(indices))


    def load_images(self, directory: str, indices: str):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")
        dir_files = os.listdir(directory)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]
        dir_files = sorted(dir_files)
        if not dir_files:
            raise FileNotFoundError(f"No valid image files found in '{directory}'.")
        index_list = self._parse_indices(indices, len(dir_files))
        if not index_list:
            raise ValueError("No valid indexes found in input or indexes out of range.")
        selected_files = [os.path.join(directory, dir_files[i]) for i in index_list]
        images = []
        masks = []
        has_non_empty_mask = False
        for path in selected_files:
            i = Image.open(path)
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image_np = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)[None,]
            if 'A' in i.getbands():
                mask_np = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask_tensor = 1. - torch.from_numpy(mask_np)
                has_non_empty_mask = True
            else:
                # Default mask, matching previous logic
                mask_tensor = torch.zeros((image_tensor.shape[2], image_tensor.shape[3]), dtype=torch.float32)
            images.append(image_tensor)
            masks.append(mask_tensor)
        image_batch = torch.cat(images, dim=0) if len(images) > 1 else images[0]
        mask_batch = torch.stack(masks, dim=0) if len(masks) > 1 else masks[0]
        return (image_batch, mask_batch, len(images))
