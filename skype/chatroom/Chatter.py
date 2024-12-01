class Chatter:
    def __init__(self, nickname, ip, port):
        self.nickname = nickname
        self.ip = ip
        self.port = port

    def __repr__(self):
        return f"{self.nickname} ({self.ip}:{self.port})"