from .ColorText import ColorText
import datetime

BOTTOM_LENGTH = 50

class ColorTools:
    color_text = ColorText
    arrow_long_left = ColorText("<=====")
    arrow_long_right = ColorText("=====>")
    arrow_left = ColorText("<=")
    arrow_right = ColorText("=>")
    pointer_left = ColorText("<-")
    pointer_right = ColorText("->")


    corners = {
        "sharp": ["┌", "┐", "┘", "└"],
        "round": ["╭", "╮", "╯", "╰"],
        "heavy": ["┏", "┓", "┛", "┗"],
        "double": ["╔", "╗", "╚", "╝"],
    }
    @staticmethod
    def disable_color(): return ColorText.disable_color()
    @staticmethod
    def enable_color(): return ColorText.enable_color()

    @staticmethod
    def arrow(direction=">", style="pointer"):
        directions = {
            ">": ">",
            "right": ">",
            "<": "<",
            "left": "<",
        }
        styles = {
            "pointer": {
                ">": ColorTools.pointer_right,
                "<": ColorTools.pointer_left,
            },
            "arrow": {
                ">": ColorTools.arrow_right,
                "<": ColorTools.arrow_left,
            },
            "long_arrow": {
                ">": ColorTools.arrow_long_right,
                "<": ColorTools.arrow_long_left,
            }
        }
        style = styles.get(style.lower(), "pointer")
        direction = directions.get(direction.lower(), ">")

        return styles[style][directions[direction]]

    @staticmethod
    def corner(style="sharp", angle="tl"):
        directions = {"tl": 0, "tr": 1, "br": 2, "bl": 3}
        style = ColorTools.corners.get(style.lower(), "sharp")
        direction = directions.get(angle.lower(), 0)
        return style[direction]

    @staticmethod
    def div(length=BOTTOM_LENGTH, color="white"):
        return ColorText("-", color) * length

    @staticmethod
    def dash(color="white"): return ColorText("-", color)
    @staticmethod
    def pipe(color="white"): return ColorText("|", color)
    @staticmethod
    def flup(color="white"): return ColorText("--|", color)
    @staticmethod
    def chunk(color="white"): return ColorText('|---|', color)

    @staticmethod
    def color(text, color="white"):
        return ColorText(text, color=color)

    @staticmethod
    def timestamp(): return ColorText(datetime.datetime.now().strftime("[%b %d | %H:%M:%S]")).red()

