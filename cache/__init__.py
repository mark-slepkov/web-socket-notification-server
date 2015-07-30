__author__ = 'mark'
import memcache as memcache

class Cache(memcache.Client):
    def exists(self, key):
        #self.flush_all()
        try:  # TODO в продакшн можно будет попробовать убрать
            value = self.get(key)
        except Exception as ex:
            value = None
        if value is None:
            result = False
        else:
            result = True
        return result

    def get_user_id(self, session_prefix, sess_id):
        user_id = 0
        sess_id_key = session_prefix + sess_id
        if (sess_id != '') and (self.exists(sess_id_key)):
            user_id = int(self.get(sess_id_key))
        return user_id

mc = Cache(['127.0.0.1:11211'])