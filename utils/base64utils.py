import base64

def base64_url_decode(data):
    data = data.encode(u'ascii')
    data += '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data)

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip('=')
