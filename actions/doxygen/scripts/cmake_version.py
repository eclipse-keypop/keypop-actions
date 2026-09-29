#!/usr/bin/env python3

"""Shared helper extracting the project version from a CMakeLists.txt file."""

import re
from pathlib import Path

_PROJECT_VERSION_PATTERN = re.compile(
    r'PROJECT\s*\([^)]*VERSION\s+(\d+\.\d+\.\d+(?:\.\d+)?)[^)]*\)', re.MULTILINE | re.IGNORECASE)


class CMakeVersionError(ValueError):
    """Raised when the project version cannot be extracted from CMakeLists.txt"""
    pass


def parse_cmake_version(cmake_file: Path) -> str:
    """
    Extract the project version from CMakeLists.txt

    The version is read from the PROJECT(... VERSION x.y.z[.t] ...) command or, as a fallback,
    from the SET(CMAKE_PROJECT_VERSION_MAJOR/MINOR/PATCH "x") declarations.

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

    content = cmake_file.read_text()

    version_match = _PROJECT_VERSION_PATTERN.search(content)
    if version_match:
        return version_match.group(1)

    parts = []
    for part in ("MAJOR", "MINOR", "PATCH"):
        part_match = re.search(
            r'SET\s*\(\s*CMAKE_PROJECT_VERSION_%s\s+"?(\d+)"?\s*\)' % part, content, re.IGNORECASE)
        if not part_match:
            raise CMakeVersionError("Could not extract PROJECT VERSION")
        parts.append(part_match.group(1))
    return ".".join(parts)
