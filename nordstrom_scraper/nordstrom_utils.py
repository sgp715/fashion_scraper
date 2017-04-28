import requests
import shutil
import imghdr


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

        if 'Content-Type' in r.headers:
            content_type = r.headers['Content-Type'].split('/')
            image = content_type[0] == 'image'
            filetype = content_type[1]
        else:
            print "No Content Type"
            return

        if not(image):
            print "Not an image"
            return

        filetypes = {'gif':'gif', 'jpeg':'jpg', 'png':'png'}
        filename = None
        if filetype in filetypes:
            filename = path + '.' + filetypes[filetype]
        else:
            print "Filetype not recognized"
            return

        data = r.raw
        with open(filename, 'wb') as f:
            data.decode_content = True
            print "writing -> " + filename
            shutil.copyfileobj(data, f)
