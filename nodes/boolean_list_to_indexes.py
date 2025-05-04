"""
    This node receives a list of bools (string) and returns indexes count (formatted for the node LoadImagesFromDirByIndexBatch)
"""

class BooleanIndexesToString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bool_list": ("STRING", {"default": ""}),
            }
        }


    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("index_string",)
    FUNCTION = "get_indexes"
    CATEGORY = "util"


    def get_indexes(self, bool_list: str):
        s = bool_list.strip().replace(" ", "")
        # If input contains any commas, split by commas
        if "," in s:
            tokens = s.split(",")
        elif all(c in "01" for c in s):
            tokens = list(s)
        elif set(s.lower()) <= set("truefalse"):
            tokens = []
            i = 0
            while i < len(s):
                if s[i:i+4].lower() == "true":
                    tokens.append("true")
                    i += 4
                elif s[i:i+5].lower() == "false":
                    tokens.append("false")
                    i += 5
                else:
                    i += 1
        else:
            tokens = []


        true_values = {"true", "1"}
        indexes = [str(i) for i, v in enumerate(tokens) if v.lower() in true_values]
        return (",".join(indexes),)
