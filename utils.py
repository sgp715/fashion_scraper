import requests
import shutil


def download_image(url, path):
    """
    given the url of an image dowload image to specified path
    """

    try:
        r = requests.get(url, stream=True)
    except:
        print "Could not load image: " + url
        return
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
