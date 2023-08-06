# MIT licensed
# Copyright (c) 2020 Francesco Russo

from pathlib import Path
from typing import Any, List
import argparse
import sys

_version = '1.0.0'

file_category = {'header_legacy': 'h', 'header': 'hpp', 'source': 'cpp'}

verbose = False


def _fetch_filenames(folder: str, extension: str) -> List[Path]:
    """
    Fetches all filenames with a certain extension from a folder and its subfolders.

    Args:
        folder: string; relative or absolute path to a folder.
        extension: string; filenames with this extension will be
            added to a list which is returned.

    Returns:
        A list of filenames (as Path objects) ending with the specified extension.

    Raises:
        ValueError: path 'folder' does not exist.
    """
    folderPath = Path(folder)

    if not folderPath.exists():
        raise ValueError(f"Path '{folder}' does not exist!")

    return list(folderPath.glob(f"**/*.{extension}"))


def _remove_include_guard(file_contents: List[str]) -> None:
    """
    Removes the include guard lines (#ifndef/#define/#endif) from a header.

    Args:
        file_contents: list of string; contents of a header file.
            This argument is modified by this function, since the
            include guard lines are removed from it.

    Returns:
        Nothing.

    Raises:
        ValueError: header has incomplete or invalid include guard.
    """
    incl_guard_indices = {'ifndef': -1, 'define': -1, 'endif': -1}
    # Find the line indices of #ifndef and #define
    found_ifndef = False
    found_define = False
    for idx in range(len(file_contents)):
        if (not found_ifndef
                and not found_define
                and file_contents[idx].startswith('#ifndef')):
            incl_guard_indices['ifndef'] = idx
            found_ifndef = True
        elif (found_ifndef
                and not found_define
                and file_contents[idx].startswith('#define')):
            incl_guard_indices['define'] = idx
            found_define = True

        if found_ifndef and found_define:
            # Leave the loop and proceed to the next stage
            break

    # Find the line index of #endif
    found_endif = False
    line_idx = -1
    while found_endif is False and -line_idx < len(file_contents):
        if file_contents[line_idx].startswith('#endif'):
            incl_guard_indices['endif'] = (len(file_contents) + line_idx)
            found_endif = True # Leave the loop
        else:
            line_idx -= 1

    # Verify that the processed header is valid
    if (incl_guard_indices['ifndef'] > incl_guard_indices['define']
            or incl_guard_indices['define'] > incl_guard_indices['endif']
            or incl_guard_indices['endif'] < incl_guard_indices['ifndef']
            or not found_ifndef or not found_define or not found_endif):
        raise ValueError("Invalid include guard!")

    # Delete from the end in order to avoid going out-of-bounds as the list length shrinks
    del file_contents[incl_guard_indices['endif']]
    del file_contents[incl_guard_indices['define']]
    del file_contents[incl_guard_indices['ifndef']]


# 'First-party headers' are the ones authored by you,
# i.e. the headers of your own library
def _remove_firstparty_includes(code: List[str], firstparty_headers: List[Path]) -> None:
    """
    Removes the includes of your own library headers, i.e. the headers authored by you.

    Args:
        code: list of string; source code to be filtered.
            This argument is modified by this function, since the includes
            are removed from it.
        firstparty_headers: list of Path; the paths (names included) to each of
            your own library headers, i.e. the headers located in the directory
            you passed to cmdline option '-e'/'--headers'.

    Returns:
        Nothing.

    Raises:
        Nothing.
    """
    # Extract first-party filenames (directory not included)
    fp_filenames = [file.name for file in firstparty_headers]

    # Replace the input list with the filtered list
    # Note: "[:]" is needed to modify the list pointed to by
    # the name 'code', otherwise we would simply make
    # 'code' point to the new list, which would then go
    # out of scope, while the input list (which remains
    # untouched) is still pointed to by the name used as
    # argument in the call to this function, and therefore
    # does not disappear.
    #
    # Explanation of the filter
    # Keep the line if:
    # - it does neither start with '#include "' nor with '#include \''
    # OR
    # - it is not a first-party include (meaning it's not an include
    #   for one of your own headers)
    code[:] = [line for line in code if
               not line.startswith('#include "')
               and not line.startswith('#include \'')
               or not any(filename in line for filename in fp_filenames)]


# It returns an argparse.Namespace object,
# but for simplicity the type hint uses "Any"
def _parse_cmdline_arguments(arguments: List[str]) -> Any:
    """
    Parses cmdline arguments given to sourcemerger.

    Args:
        arguments: list of string; arguments to be parsed.

    Returns:
        An argparse.Namespace object, whose member variables contain
        the values passed to the various cmdline options.

    Raises:
        Nothing.
    """
    parser = argparse.ArgumentParser(prog="sourcemerger",
                                     description="This tool produces a single-header, "
                                     "single-implementation-file C++ library from your "
                                     "source code.")
    parser.add_argument("-e", "--headers",
                        type=Path, dest='headers_folder', required=True,
                        help="Path to the folder that contains the headers (both .h "
                        "and .hpp headers are supported)")
    parser.add_argument("-s", "--sources",
                        type=Path, dest='impl_folder', required=True,
                        help="Path to the folder that contains the implementation files "
                             "(i.e. the sources)")
    parser.add_argument("-n", "--name",
                        type=str, dest='library_name', required=True,
                        help="Name of the output library files (.h and .cpp are appended "
                             "automatically)")
    parser.add_argument("-d", "--dest",
                        type=Path, dest='dest_folder', required=False, default='.',
                        help="Path to save the output files in (default is current dir)")
    parser.add_argument("-v", "--verbose",
                        action='store_true', dest='verbose', required=False,
                        help="Enable verbose output")
    parser.add_argument("--version",
                        action='version', version=_version)
    return parser.parse_args(arguments)


def merge_files(headers_folder: str, impl_folder: str,
                library_name: str, dest_folder: str, verbose: bool) -> None:
    """
    Merges your .h/.hpp files into one, and your .cpp files into one.

    This is the core logic of sourcemerger: it calls all other functions
    to fetch the filenames of your library headers and implementation files,
    remove include guards and include lines for your library headers and,
    lastly, concatenate them into one header file and one implementation file.
    The single header file is given an include guard of its own, and the
    single implementation file is given an include line for the single header file.
    These two files are then written to disk, and the program quits.

    Args:
        headers_folder: string; path to the folder that contains the headers.
        impl_folder: string; path to the folder that contains the implementation files.
        library_name: string; name of the output library files.
        dest_folder: string; path to save the output files in.
        verbose: string; enable verbose output.

    Returns:
        Nothing.

    Raises:
        Nothing.
    """

    # Set program-level verbosity
    if verbose:
        print("Starting sourcemerger")

    # Set the names of the output .h and .cpp library files
    out_header_name = library_name + '.h'
    out_impl_name = library_name + '.cpp'

    # Generate the include guard strings from the name
    out_header_include_guards = ['#ifndef ' + library_name.upper() + '_H\n',
                                 '#define ' + library_name.upper() + '_H\n',
                                 '#endif // ' + library_name.upper() + '_H\n']

    dest_folder = Path(dest_folder)
    # Set up the path of the single header 'cinac.h'
    # by appending ("/") its name to the Path object
    out_header = dest_folder / out_header_name

    # Generate the single header 'cinac.h'
    with open(str(out_header), 'w') as outfile:
        # Write '#ifndef...' and '#define...'
        outfile.writelines(out_header_include_guards[:2])

        headers_folder = Path(headers_folder)
        # Get a list of all headers (have one copy as Path objects
        # and one copy as strings; both are needed)
        header_paths = _fetch_filenames(headers_folder, file_category['header'])
        header_paths = header_paths + _fetch_filenames(headers_folder,
                                                       file_category['header_legacy'])
        header_list = [str(path_object) for path_object in header_paths]
        header_list = sorted(header_list, key=str.lower) # Case-insensitive sort

        # Loop through each header
        for filename in header_list:
            if verbose:
                print(f"Now working on header '{filename}'")
            # Read the file into a list (memory-inefficient, I know, but
            # I expect headers to be at most 1 MB)
            with open(filename, 'r') as file:
                file_contents = file.readlines()

            _remove_include_guard(file_contents)
            _remove_firstparty_includes(file_contents, header_paths)

            # Flush the include-guard-less header into the single header
            outfile.writelines(file_contents)
            outfile.write('\n')

        # Write '#endif...'
        outfile.writelines(out_header_include_guards[2])
    if verbose:
        print(f"Generated single header '{str(out_header)}'")

    # Set up the path of the single implementation file 'cinac.cpp'
    # by appending ("/") its name to the Path object
    out_impl_file = dest_folder / out_impl_name

    # Generate the single implementation file 'cinac.cpp'
    with open(str(out_impl_file), 'w') as outfile:
        # Write an include for the single header
        outfile.write(f'#include "{out_header_name}"\n')

        impl_folder = Path(impl_folder)
        # Get a list of all implementation files
        impl_file_list = _fetch_filenames(impl_folder, file_category['source'])
        impl_file_list = [str(path_object) for path_object in impl_file_list]
        impl_file_list = sorted(impl_file_list, key=str.lower) # Case-insensitive sort

        # Loop through each implementation file
        for filename in impl_file_list:
            if verbose:
                print(f"Now working on impl. file '{filename}'")
            # Read the file into a list (memory-inefficient, I know)
            with open(filename, 'r') as file:
                file_contents = file.readlines()

            _remove_firstparty_includes(file_contents, header_paths)

            # Flush the filtered impl. file into the single impl. file
            outfile.writelines(file_contents)
            outfile.write('\n')

    if verbose:
        print(f"Generated single implementation file '{str(out_impl_file)}'")
        print("Merging complete!")


def _cmdline_tool_main():
    parsed_args = _parse_cmdline_arguments(sys.argv[1:])
    merge_files(parsed_args.headers_folder,
                parsed_args.impl_folder,
                parsed_args.library_name,
                parsed_args.dest_folder,
                parsed_args.verbose)
