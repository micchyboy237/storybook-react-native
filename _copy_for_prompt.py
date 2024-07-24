import os
import fnmatch
import argparse
import subprocess

DEFAULT_MESSAGE = "Analyze all files above then derive the business requirements categorized by features"

# Default exclude files or directories with wildcard support
exclude_files = [
    '*node_modules*',
]

include_files = [
    'package.json'
]


def find_files(base_dir, include, exclude):
    matched_files = []
    for root, dirs, files in os.walk(base_dir):
        # Exclude specified directories with wildcard support
        dirs[:] = [d for d in dirs if not any(
            fnmatch.fnmatch(os.path.join(root, d), pat) for pat in exclude)]

        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), base_dir)
            if (any(fnmatch.fnmatch(file, pat) for pat in include) or any(fnmatch.fnmatch(file_path, pat) for pat in include)) and not any(fnmatch.fnmatch(file_path, pat) for pat in exclude):
                matched_files.append(file_path)
                print(f"Matched file: {file_path}")
            # else:
                # print(f"Skipped file: {file_path}")
    return matched_files


def main():
    global exclude_files, include_files

    print("Running _copy_for_prompt.py")
    # Parse command-line options
    parser = argparse.ArgumentParser(
        description='Generate clipboard content from specified files.')
    parser.add_argument('-b', '--base-dir', default=os.getcwd(),
                        help='Base directory to search files in (default: current directory)')
    parser.add_argument('-i', '--include', nargs='*', default=include_files,
                        help='Patterns of files to include (default: server.ts, user*)')
    parser.add_argument('-e', '--exclude', nargs='*', default=exclude_files,
                        help='Directories or files to exclude (default: node_modules)')
    parser.add_argument('-m', '--message', default=DEFAULT_MESSAGE,
                        help='Message to include in the clipboard content')
    parser.add_argument('-fo', '--filenames-only', action='store_true',
                        help='Only copy the relative filenames, not their contents')

    args = parser.parse_args()
    base_dir = args.base_dir
    include = args.include
    exclude = args.exclude
    message = args.message
    filenames_only = args.filenames_only

    # Update global lists
    include_files = include
    exclude_files = exclude

    # Find all files matching the patterns in the base directory and its subdirectories
    print("\n")
    files = find_files(base_dir, include, exclude)

    print("\n")
    print(f"Base directory: {base_dir}")
    print(f"Include patterns: {include}")
    print(f"Exclude patterns: {exclude}")
    print(f"Filenames only: {filenames_only}")
    print(f"\nFound files ({len(files)}): {files}")
    print(f"\nMessage: {message}")

    if not files:
        print("No files found matching the given patterns.")
        return
    print("\n")

    # Initialize the clipboard content
    clipboard_content = ""

    # Append relative filenames to the clipboard content
    for file in files:
        prefix = (
            f"## Relative path: {file}\n" if not filenames_only else f"{file}\n")
        if filenames_only:
            clipboard_content += f"{prefix}"
        else:
            file_path = os.path.join(base_dir, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    clipboard_content += (
                        f"{prefix}{f.read()}\n\n")
            else:
                clipboard_content += f"{prefix}\n"

    # Append the message to the clipboard content
    clipboard_content += f"\n{message}"
    # Add a newline at the end
    clipboard_content += "\n"

    # Print the content to the console for manual copying (if needed)
    # print(clipboard_content)

    # Copy the content to the clipboard
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(clipboard_content.encode('utf-8'))


if __name__ == "__main__":
    main()

# Sample usage:
# python _copy_for_prompt.py -m "Check if anything's wrong"
