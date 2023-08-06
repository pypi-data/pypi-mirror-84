import requests


class BaseClient:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = "http://{}:{}/".format(ip, port)
        self.session = requests.Session()

    def get(self, path):
        return self.session.get(self.url + path)

    def post(self, path, **data):
        return self.session.post(self.url + path, data=data)

