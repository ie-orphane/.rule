class Colorful:
    def __init__(self) -> None:
        __COLORS = [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
        ]

        for i in range(8):
            exec(
                "@staticmethod\n"
                f"def {__COLORS[i]}(text: str, bold: bool = True, /):\n"
                f"\treturn f'\x1b[{"{int(bold)}"};3{i}m{"{text}"}\x1b[0m'\n"
                f"self.{__COLORS[i]} = {__COLORS[i]}"
            )

    @staticmethod
    def black(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def red(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def green(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def yellow(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def blue(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def magenta(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def cyan(text: str, bold: bool = True, /) -> str: ...

    @staticmethod
    def white(text: str, bold: bool = True, /) -> str: ...


COLORFUL = Colorful()


__all__ = ["COLORFUL"]
