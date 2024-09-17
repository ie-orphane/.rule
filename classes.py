from colorful import COLORFUL

__all__ = ["Guardian", "Log"]


class Guardian:
    def __init__(self) -> None:
        self.ignore = False
        self.exit_code = 0


class Log:
    def __init__(self) -> None:
        self.errors = []
        self.max = 0

    def error(self, name: str, /, *, line: str, col: int = None):
        self.max = max(self.max, len(name))
        self.errors.append(
            (name, f"(line {line:>2}{f", col {col:>2})" if col else ")"}")
        )

    @staticmethod
    def show_index(index: int, count: int):
        if index >= 7:
            return COLORFUL.blue(f"  [{index:>0{len(str(count))}}]  ")
        return COLORFUL.cyan(f"  [{index:>0{len(str(count))}}]  ")

    def log(self, file_name: str, /):
        errors_count = len(self.errors)
        if errors_count == 0:
            print(f"✅  {COLORFUL.white(file_name)}  {COLORFUL.green('Ok')}")
            return

        print(
            f"❌  {COLORFUL.white(file_name)}  {COLORFUL.red('Error')}",
            *[
                self.show_index(index, errors_count) + f"{name:<{self.max}}  {detailes}"
                for index, (name, detailes) in enumerate(self.errors, 1)
            ],
            sep="\n",
        )

    @property
    def exit_code(self):
        if len(self.errors) == 0:
            return 0
        return 1
