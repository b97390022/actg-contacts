import glob
import editdistance


def get_file_path(root_path: str, file_name: str):
    file_path = glob.glob(f"{root_path}/**/{file_name}", recursive=True)
    return file_path[0]


def caculate_editdistance(a: str, b: str):
    return editdistance.distance(a, b)
