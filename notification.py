__author__ = 'mark'
import json
TYPES = {'MESSAGE': 0,
         'FRIENDSHIP': 1,
         'GIFT': 2}


class Notification:
    notification = dict()

    def __init__(self, users, notification_type, content=None, **kwargs):
        if type(users) == list:
            self.notification['users'] = users
        elif type(users) == int:
            self.notification['users'] = list()
            self.notification['users'].append(users)
        else:
            raise Exception
        self.notification['type'] = notification_type
        self.notification['content'] = content
        for key, value in kwargs.items():
            self.notification[key] = value

    def to_string(self):
        return json.dumps(self.notification)

    def to_bytes(self):
        return json.dumps(self.notification).encode()