"""
    This node receives a list of bools (string or bools) and returns indexes count (formatted for the node LoadImagesFromDirByIndexBatch)
"""

class BooleanIndexesToString:
    memory_bools: list[bool] = []
    pending_reset: bool = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "bool_list_str": ("STRING", {"default": ""}),
                "bool_list": ("BOOLEAN[]", {"default": []}),
                "memory_bool_list_str": ("STRING", {"default": ""}),
                "memory_bool_list": ("BOOLEAN[]", {"default": []}),
                "reset": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("index_string",)
    FUNCTION = "get_indexes"
    CATEGORY = "util"

    @staticmethod
    def parse_bool_string(s: str) -> list[bool]:
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

    def get_indexes(
        self,
        bool_list_str: str = "",
        bool_list=None,
        memory_bool_list_str: str = "",
        memory_bool_list=None,
        reset: bool = False,
    ):
        if bool_list is None:
            bool_list = []
        if memory_bool_list is None:
            memory_bool_list = []

        if self.__class__.pending_reset:
            self.__class__.memory_bools.clear()
            self.__class__.pending_reset = False

        if bool_list_str:
            new_bools = self.parse_bool_string(bool_list_str)
        elif bool_list:
            new_bools = list(bool_list)
        elif memory_bool_list_str:
            new_bools = self.parse_bool_string(memory_bool_list_str)
        elif memory_bool_list:
            new_bools = list(memory_bool_list)
        else:
            new_bools = []

        self.__class__.memory_bools += new_bools

        self.__class__.pending_reset = reset

        indexes = [str(i) for i, v in enumerate(self.__class__.memory_bools) if v]
        output = ",".join(indexes)
        return (output,)


