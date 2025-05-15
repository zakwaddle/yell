import re
from .AnsiColors import AnsiColors

class ColorText:
    use_color = True
    ansi = AnsiColors()
    """A class for creating and managing colored text using ANSI color codes.

    This class allows you to create text with various foreground and background colors
    using ANSI escape sequences. It provides methods for changing colors and supports
    method chaining for convenient color modifications.

    Example:
        text = ColorText("Hello")
        print(text.red()) # prints in red
        print(text.bg_blue()) # prints with a blue background
    """
    
    @classmethod
    def disable_color(cls):
        cls.use_color = False
    
    @classmethod
    def enable_color(cls):
        cls.use_color = True
        
    @staticmethod
    def find_length(text):
        """Find the length of the pre-concatenated string with ANSI color codes."""
        # Remove all ANSI escape sequences
        clean_text = re.sub(r'\033\[[0-9;]*[a-zA-Z]', '', string=text)
        return len(clean_text)

    @staticmethod
    def find_ansi_offset(text):
        """Find the number of ANSI escape sequences in the text."""
        matches = re.findall(r'\033\[[0-9;]*m', string=text)
        return sum(len(match) for match in matches)

    def __init__(self, text, color="white", bg=None):
        self._text = text
        self._fg = color
        self._bg = bg

    def __str__(self):
        """Convert the ColorText instance to a string with ANSI color codes.

        Returns:
            str: The text with applied ANSI color formatting
        """
        if not ColorText.use_color:
            return self._text
        try:
            if self._bg is not None and not self._bg.startswith("bg_") :
                self._bg = f"bg_{self._bg}"
            return AnsiColors().colorize(self._fg, self._text, self._bg)
        except Exception as e:
            print(f"Error: {e}")
            return self._text

    def __repr__(self):
        """Get the string representation of the ColorText instance.

        Returns:
            str: A string representation showing the text content
        """
        return f"<ColorText: {self._text}>"

    def __add__(self, other):
        """Add another ColorText instance to this instance."""
        return str(self) + str(other)

    def __radd__(self, other):
        """Add another ColorText instance to this instance."""
        return str(other) + str(self)

    def __mul__(self, other):
        """Multiply the text content by a number."""
        new_text = self._text * other
        text = ColorText(new_text, color=self._fg, bg=self._bg)
        return str(text)
        # return self.__text * other


    def __rmul__(self, other):
        """Multiply the text content by a number."""
        text = ColorText(self._text * other)
        text.set_fg(self._fg)
        text.set_bg(self._bg)
        return text

    def __len__(self):
        """Get the length of the text content."""
        return len(self._text)

    def __getitem__(self, index):
        """Get the character at the given index."""
        return self._text[index]

    def __setitem__(self, index, value):
        """Set the character at the given index."""
        self._text = self._text[:index] + value + self._text[index + 1:]

    def __delitem__(self, index):
        """Delete the character at the given index."""
        self._text = self._text[:index] + self._text[index + 1:]

    def __call__(self, text):
        """Update the text content when the instance is called as a function.

        Args:
            text (str): New text to set

        Returns:
            ColorText: The instance with updated text
        """
        self._text = text
        return self

    def set_fg(self, color):
        """Set the foreground color."""
        if AnsiColors().is_valid(color):
            self._fg = color
        return self

    def set_bg(self, color):
        """Set the background color."""
        if color is None:
            self._bg = None
            return self
        if not color.startswith("bg_"):
            color = f"bg_{color}"
        if AnsiColors().is_valid(color):
            self._bg = color
        return self

    def white(self):
        """Set the text color to white.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "white"
        return self

    def red(self):
        """Set the text color to red.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "red"
        return self

    def green(self):
        """Set the text color to green.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "green"
        return self

    def yellow(self):
        """Set the text color to yellow.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "yellow"
        return self

    def blue(self):
        """Set the text color to blue.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "blue"
        return self

    def magenta(self):
        """Set the text color to magenta.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "magenta"
        return self

    def cyan(self):
        """Set the text color to cyan.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "cyan"
        return self

    def bright_white(self):
        """Set the text color to bright white.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_white"
        return self

    def bright_red(self):
        """Set the text color to bright red.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_red"
        return self

    def bright_green(self):
        """Set the text color to bright green.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_green"
        return self

    def bright_yellow(self) -> "ColorText":
        """Set the text color to bright yellow.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_yellow"
        return self

    def bright_blue(self) -> "ColorText":
        """Set the text color to bright blue.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_blue"
        return self

    def bright_magenta(self) -> "ColorText":
        """Set the text color to bright magenta.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_magenta"
        return self

    def bright_cyan(self) -> "ColorText":
        """Set the text color to bright cyan.

        Returns:
            ColorText: The instance with updated color
        """
        self._fg = "bright_cyan"
        return self

    def bg_white(self) -> "ColorText":
        """Set the background color to white.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_white"
        return self

    def bg_red(self) -> "ColorText":
        """Set the background color to red.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_red"
        return self

    def bg_green(self) -> "ColorText":
        """Set the background color to green.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_green"
        return self

    def bg_yellow(self) -> "ColorText":
        """Set the background color to yellow.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_yellow"
        return self

    def bg_blue(self) -> "ColorText":
        """Set the background color to blue.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_blue"
        return self

    def bg_magenta(self) -> "ColorText":
        """Set the background color to magenta.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_magenta"
        return self

    def bg_cyan(self) -> "ColorText":
        """Set the background color to cyan.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_cyan"
        return self

    def bg_bright_white(self) -> "ColorText":
        """Set the background color to bright white.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_white"
        return self

    def bg_bright_red(self) -> "ColorText":
        """Set the background color to bright red.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_red"
        return self

    def bg_bright_green(self) -> "ColorText":
        """Set the background color to bright green.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_green"
        return self

    def bg_bright_yellow(self) -> "ColorText":
        """Set the background color to bright yellow.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_yellow"
        return self

    def bg_bright_blue(self) -> "ColorText":
        """Set the background color to bright blue.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_blue"
        return self

    def bg_bright_magenta(self) -> "ColorText":
        """Set the background color to bright magenta.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_magenta"
        return self

    def bg_bright_cyan(self) -> "ColorText":
        """Set the background color to bright cyan.

        Returns:
            ColorText: The instance with updated background color
        """
        self._bg = "bg_bright_cyan"
        return self

    def reset_fg(self) -> "ColorText":
        """Reset the foreground color to 'default'."""
        self._fg = "white"
        return self

    def reset_bg(self) -> "ColorText":
        """Reset the background color to 'default'."""
        self._bg = None
        return self

    def reset(self) -> "ColorText":
        """Reset both foreground and background colors to 'default'.

        Returns:
            ColorText: The instance with reset colors
        """
        self._fg = "white"
        self._bg = None
        return self
