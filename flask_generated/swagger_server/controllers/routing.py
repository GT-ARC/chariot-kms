import connexion


class RoutingInformation():
    def __init__(self, base_url="", routing_url="", base_kafka="", routing_kafka=""):
        self.base_url = base_url
        self.routing_url = routing_url
        self.base_kafka = base_kafka
        self.routing_kafka = routing_kafka
        self.breadcrumbs_url = [base_url, ]
        self.breadcrumbs_kafka = [base_kafka, ]
    
    @staticmethod
    def create_root_routing_object():
        r = RoutingInformation(base_url=connexion.request.url_root + connexion.request.blueprint[1:] + "/",
                               routing_url=connexion.request.url,
                               base_kafka='kms.global.',
                               routing_kafka='')
        return r
    
    def add(self, crumb):
        '''
        add a crumb to the path to remember where the serializer has been
        @param crumb:
        @return:
        '''
        self.breadcrumbs_url.append(crumb)
        self.breadcrumbs_kafka.append(crumb)
    
    def up(self):
        '''
        go back up
        @return:
        '''
        try:
            self.breadcrumbs_url.pop()
            self.breadcrumbs_kafka.pop()
        except:
            pass
    
    def urlize(self, d: dict):
        d['url'] = self._get_url()
        d['kafka_topic'] = self._get_kafka()
    
    def _get_url(self):
        return "".join(self.breadcrumbs_url)
    
    def _get_kafka(self):
        return "".join(self.breadcrumbs_kafka).replace("/", ".")
    
    def new_root(self, url, kafka):
        self.base_url = url
        self.breadcrumbs_url = [url, ]
        self.base_kafka = kafka
        self.breadcrumbs_kafka = [kafka, ]
