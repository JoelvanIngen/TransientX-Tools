import os
import shutil


def list_ext_files(ext: str, directory: str = None) -> tuple[list[str], list[str]]:
    """
    List all files with a specified extension in a directory and returns both the filename and the path
    :param ext: file extension to search for
    :param directory: directory to look in
    :return: tuple of paths and filenames
    """
    paths = []
    files = []
    for f in os.listdir(directory):
        if f.endswith(ext):
            files.append(f)
            paths.append(os.path.join(directory, f) if directory else f)

    return paths, files


def copy_file(src: str, dst_dir: str, filename: str) -> None:
    dest = os.path.join(dst_dir, filename)

    # Create destination folder if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # copy2 as opposed to copyfile preserves metadata
    shutil.copy2(src, dest)


def add_to_filename(filename: str, suffix) -> str:
    filename_split = filename.split('.')
    name, ext = '.'.join(filename_split[:-1]), filename_split[-1]
    return f'{name}_{suffix}.{ext}'
