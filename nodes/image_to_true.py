"""
    This node simply outputs true when receives an image, used for automation
"""

class ImageToTrue:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "process"
    CATEGORY = "northTools"

    def process(self, image):
        return (True,)

