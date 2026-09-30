#!/usr/bin/env python3

"""Shared helper extracting the project version from a CMakeLists.txt file."""

import re
from pathlib import Path

_PROJECT_VERSION_PATTERN = re.compile(
    r'\bPROJECT\s*\([^)]*VERSION\s+(\d+\.\d+\.\d+(?:\.\d+)?)[^)]*\)', re.MULTILINE | re.IGNORECASE)
_BRACKET_OPEN_PATTERN = re.compile(r'\[(=*)\[')


class CMakeVersionError(ValueError):
    """Raised when the project version cannot be extracted from CMakeLists.txt"""
    pass


def strip_cmake_comments(content: str) -> str:
    """
    Remove CMake line comments (# ...) and bracket comments (#[[ ... ]], #[=[ ... ]=]) from content

    Quoted arguments and bracket arguments are preserved, so a '#' inside them is not treated as
    the start of a comment.
    """
    result = []
    i = 0
    length = len(content)
    while i < length:
        char = content[i]
        if char == '"':
            # Quoted argument, copied as is (backslash escapes the next character)
            end = i + 1
            while end < length and content[end] != '"':
                end += 2 if content[end] == '\\' else 1
            result.append(content[i:end + 1])
            i = end + 1
        elif char == '[' and _BRACKET_OPEN_PATTERN.match(content, i):
            # Bracket argument, copied as is
            equals = _BRACKET_OPEN_PATTERN.match(content, i).group(1)
            end = content.find(f"]{equals}]", i)
            end = length if end < 0 else end + len(equals) + 2
            result.append(content[i:end])
            i = end
        elif char == '#':
            bracket = _BRACKET_OPEN_PATTERN.match(content, i + 1)
            if bracket:
                # Bracket comment
                closing = f"]{bracket.group(1)}]"
                end = content.find(closing, i)
                i = length if end < 0 else end + len(closing)
            else:
                # Line comment, the newline is kept
                end = content.find('\n', i)
                i = length if end < 0 else end
        else:
            result.append(char)
            i += 1
    return "".join(result)


def parse_cmake_version(cmake_file: Path) -> str:
    """
    Extract the project version from CMakeLists.txt

    The version is read from the PROJECT(... VERSION x.y.z[.t] ...) command or, as a fallback,
    from the SET(CMAKE_PROJECT_VERSION_MAJOR/MINOR/PATCH[/TWEAK] "x") declarations.

    Args:
        cmake_file: Path to CMakeLists.txt

    Returns:
        str: Version string in format x.y.z[.t]

    Raises:
        FileNotFoundError: If CMakeLists.txt doesn't exist
        CMakeVersionError: If version cannot be extracted
    """
    if not cmake_file.exists():
        raise FileNotFoundError(f"CMakeLists.txt not found at {cmake_file}")

    content = strip_cmake_comments(cmake_file.read_text())

    version_match = _PROJECT_VERSION_PATTERN.search(content)
    if version_match:
        return version_match.group(1)

    parts = []
    for part in ("MAJOR", "MINOR", "PATCH", "TWEAK"):
        part_match = re.search(
            r'\bSET\s*\(\s*CMAKE_PROJECT_VERSION_%s\s+"?(\d+)"?\s*\)' % part, content, re.IGNORECASE)
        if part_match:
            parts.append(part_match.group(1))
        elif part != "TWEAK":
            raise CMakeVersionError("Could not extract PROJECT VERSION")
    return ".".join(parts)
