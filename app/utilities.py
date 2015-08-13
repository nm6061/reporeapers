import json


def read(jsonfile):
    """Read a JSON file.

    Parameters
    ----------
    jsonfile : file object
        An open file handle to a JSON file.

    Return
    ------
    jsondata : dict
        A dictionary returned by the json.load()
    """
    jsondata = dict()
    try:
        if jsonfile:
            jsondata = json.load(jsonfile)
        return jsondata
    except:
        raise Exception('Failure in loading JSON data {0}'.format(
            jsonfile.name
        ))
    finally:
        jsonfile.close()