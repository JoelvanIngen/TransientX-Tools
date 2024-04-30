import os


def list_ext_files(ext: str, directory: str = None) -> list[str]:
    files = []
    for f in os.listdir(directory):
        if f.endswith(ext):
            files.append(os.path.join(directory, f) if directory else f)

    return files
