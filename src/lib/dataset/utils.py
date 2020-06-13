
import glob
from os import path

def get_categories(sample_answers):
    """
    Gets [[key,key],[key, key]] from [{ answers: { key: [string] }}]
    """
    return [
        [
            y["key"] for y in x["answers"]
        ] for x in sample_answers
    ]


def zeros_for(double_lst):
	return [ [ 0 for _ in lst] for lst in double_lst ]


def get_paths(raw_data_dir):
    """
    Returns zipped (png_path, json_path) for all the labeled
    data in the data dir passed in, and cuts


    The chief assumption here is that the PNGs and JSONS
    are in the same folder and named such that sorting them
    will match like with like.
    """
    data_dir = path.join(raw_data_dir, "labeled")

    png_names = glob.glob(data_dir + "/*.png")
    json_names = glob.glob(data_dir + "/*.json")
    if (len(png_names) != len(json_names)):
        msg = "Must have equal number of PNGs and JSONS; potential data corruption."
        raise Exception(msg)

    png_names.sort()
    json_names.sort()

    data_paths = list(zip(png_names, json_names))
    for png_name, json_name in data_paths:
        if png_name[0:40] != json_name[0:40]:
            msg = "PNG and JSON names do not match; potential data corruption."
            raise Exception(msg)

    return data_paths



def clip_by_range(lst, range):
    """
    Returns elements of lst clipped to a range;
    [0, 0.5] would return first half of lst.
    """
    range_start = int(range[0] * len(lst))
    range_end = int(range[1] * len(lst))
    return lst[range_start:range_end]


