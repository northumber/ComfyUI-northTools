import json
import ast

"""
    This node extract the value of a metadata input json using a 'key' input, returning the value of the key.
"""


class ExtractMetadataByKey:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "metadata": ("STRING",),
                "key": ("STRING",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)

    FUNCTION = "extract"
    CATEGORY = "northTools"

    def extract(self, metadata, key):
        try:
            data = ast.literal_eval(metadata)
        except Exception:
            try:
                data = json.loads(metadata.replace("'", "\""))
            except Exception:
                return ("" ,)
        if not key:
            return (str(data),)
        value = data.get(key, "")
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        value = value.encode('utf-8').decode('unicode_escape')
        return (str(value),)

