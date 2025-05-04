"""
    This node receives a list of bools (string or bools) and returns indexes count (formatted for the node LoadImagesFromDirByIndexBatch)
"""

class BooleanIndexesToString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bool_list_str": ("STRING", {"default": ""}),  # flexible format: TrueFalseTrue, 101, True,False,True, etc.
                "bool_list": ("BOOLEAN[]", {"default": []}),   # explicit list: [True, False, True]
            }
        }


    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("index_string",)
    FUNCTION = "get_indexes"
    CATEGORY = "util"


    @staticmethod
    def parse_bool_string(s):
        s = s.strip().replace(" ", "")
        if "," in s:
            tokens = s.split(",")
        elif all(c in "01" for c in s) and s:
            tokens = list(s)
        elif set(s.lower()) <= set("truefalse") and s:
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
        return [t.lower() in true_values for t in tokens]


    def get_indexes(self, bool_list_str: str, bool_list):
        if bool_list and len(bool_list) > 0:
            bools = bool_list
        else:
            bools = self.parse_bool_string(bool_list_str)
        indexes = [str(i) for i, v in enumerate(bools) if v]
        return (",".join(indexes),)

