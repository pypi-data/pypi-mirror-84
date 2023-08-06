class Ad(object):
    def __init__(self, host="https://www.yapo.cl"):
        self.host = host
        
    def get_ad_url(self, list_id):
        return "{}/vi/{}".format(self.host, list_id)