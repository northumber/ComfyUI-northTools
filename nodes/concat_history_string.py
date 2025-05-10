"""
   This node receives a boolean and a string, and concatenates them to a string, that is remembered in the various runs.
"""


class ConcatHistoryString:
    history = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "value_bool": ("BOOLEAN", {"default": None}),
                "value_str": ("STRING", {"default": ""}),
                "reset": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("concatenated",)
    FUNCTION = "concat"
    CATEGORY = "util"

    def concat(self, value_bool=None, value_str="", reset=False):
        if reset:
            self.__class__.history = []

        input_value = None
        if value_bool is not None:
            input_value = "True" if value_bool else "False"
        elif value_str != "":
            input_value = str(value_str)

        if input_value not in (None, ""):
            self.__class__.history.append(input_value)

        return (",".join(self.__class__.history),)




