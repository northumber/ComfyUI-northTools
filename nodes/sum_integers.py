"""
    This node sum two integers, can be inputted and outputted as int or string
"""


class SumIntegers:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int_1": ("INT", {"default": 0, "min": 0, "step": 1}),
                "int_2": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("sum_int", "sum_str")
    FUNCTION = "sum"
    CATEGORY = "northTools"

    def sum(self, int_1, int_2):
        s = int_1 + int_2
        return (s, str(s))

