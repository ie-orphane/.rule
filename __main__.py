import sys
import os
import glob
import string
from colorful import COLORFUL
from classes import Log, Guardian


ERRORS = ["CONSECUTIVE_SPACE", "EMPTY_LINE", "ONE_INSTRUCTION_PER_LINE"]
MAX_INDENT_ERROR = max([len(error) for error in ERRORS], default=0)
GUARDIAN = Guardian()
FILE_PATHS = (
    glob.glob("**/*.sh", recursive=True) if len(sys.argv) == 1 else sys.argv[1:]
)


for file_path in FILE_PATHS:
    LOG = Log()
    file_name = os.path.basename(file_path)

    try:
        with open(file_path, "r") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(
            f"✋  {COLORFUL.white(file_name, True)}  {COLORFUL.yellow("NotFound", True)}"
        )
        GUARDIAN.exit_code = 1
        continue

    # check double spaces
    file_lines = file_content.splitlines(keepends=True)

    indent = 0
    for index, line in enumerate(file_lines, 1):
        if any(
            [
                word in ["done", "fi", "esac", "elif", "else", "}"]
                for word in line.split()
            ]
        ):
            indent -= 1

        if '"""' in line:
            GUARDIAN.ignore = not GUARDIAN.ignore

        if GUARDIAN.ignore:
            continue

        # check multiple instruction (no ;)
        if ";" in line:
            line_rest = line[line.index(";") :].split()

            if (
                line[line.index(";") + 1] != ";"
                and "then" not in line_rest
                and "do" not in line_rest
                and line[line.index(";") - 1] != "\\"
            ):
                LOG.error("ONE_INSTRUCTION_PER_LINE", line=index)

        # check the exception of an empty line:
        # - after: done, fi, declare, local, {, ;;
        # - before: if, for, while, function, }
        if line == "\n" and index != 1:
            previous_line_words = file_lines[index - 2].strip().split()
            next_line_words = file_lines[index].strip().split()

            if all(
                [
                    word
                    not in [
                        "#!/bin/bash",
                        "done",
                        "fi",
                        "declare",
                        "local",
                        "{",
                        ";;",
                        "esac",
                    ]
                    for word in previous_line_words
                ]
            ) and all(
                [
                    word not in ["if", "for", "while", "function", "case"]
                    for word in next_line_words
                ]
            ):
                LOG.error("EMPTY_LINE", line=index)

        else:
            # check indentation
            count = 0
            for letter in line:
                if letter != "\t":
                    break
                count += 1

            if indent > count:
                LOG.error("MISSING_INDENT_LEVEL", line=index)

            line = line.replace("\t", "", indent - 1)

            # check empty line
            if all([letter in string.whitespace for letter in line]):
                LOG.error("EMPTY_LINE", line=index)

        check_space = True
        for current, next, col in zip(line, line[1:], range(1, len(line) + 1)):
            if current == '"':
                check_space = not check_space

            # check consecutive spaces
            if check_space and current in [" ", "\t"] and next in ["\t", " ", "\n"]:
                LOG.error("CONSECUTIVE_SPACE", line=index, col=col)

        if any([word in [";;"] for word in line.split()]):
            indent -= 1

        if any(
            [
                word in ["then", "else", "case", "do", "function", ")"]
                for word in line.split()
            ]
        ):
            indent += 1

    LOG.log(os.path.basename(file_path))

    if GUARDIAN.exit_code == 0:
        GUARDIAN.exit_code = LOG.exit_code

exit(GUARDIAN.exit_code)
