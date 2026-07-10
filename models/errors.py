class NotExistsError(Exception):
    pass


class NetworkError(Exception):
    pass

class InvalidPassError(Exception):
    pass


class NeedCaptcha(Exception):
    def __init__(self, imageUrl, capSid, capField, redirect):
        self.imageUrl = imageUrl
        self.capSid = capSid
        self.capField = capField
        self.redirect = redirect
        from json import dumps
        self.dumps = dumps

    def __str__(self):
        return self.dumps({
            "imageUrl": self.imageUrl,
            "capSid": self.capSid,
            "capField": self.capField,
            "redirect": self.redirect,
        })
