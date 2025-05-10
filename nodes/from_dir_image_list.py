import os
import numpy as np
import torch
from PIL import Image, ImageOps

"""
    Forked from ComfyUI-InspirePack
"""


class LoadImagesFromDirList:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "image_load_cap": ("INT", {"default": 0, "min": 0, "step": 1}),
                "start_index": ("INT", {"default": 0, "min": 0, "step": 1}),
                "load_always": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "INT")
    RETURN_NAMES = ("IMAGE", "MASK", "FILE PATH", "METADATA", "INDEX COUNT")
    OUTPUT_IS_LIST = (True, True, True, True, True)
    FUNCTION = "load_images"
    CATEGORY = "image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if 'load_always' in kwargs and kwargs['load_always']:
            return float("NaN")
        else:
            return hash(frozenset(kwargs))

    def load_images(self, directory: str, image_load_cap: int = 0, start_index: int = 0, load_always=False):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")

        dir_files = os.listdir(directory)
        if len(dir_files) == 0:
            raise FileNotFoundError(f"No files in directory '{directory}'.")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]
        dir_files = sorted(dir_files)
        dir_files_full = [os.path.join(directory, x) for x in dir_files]
        dir_files_full = dir_files_full[start_index:]

        images = []
        masks = []
        file_paths = []
        metadatas = []
        indexes = []

        limit_images = image_load_cap > 0
        image_count = 0

        for idx, image_path in enumerate(dir_files_full):
            if os.path.isdir(image_path):
                continue
            if limit_images and image_count >= image_load_cap:
                break

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
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            images.append(image)
            masks.append(mask)
            file_paths.append(str(image_path))
            indexes.append(idx + start_index)
            image_count += 1

        return (images, masks, file_paths, metadatas, indexes)
