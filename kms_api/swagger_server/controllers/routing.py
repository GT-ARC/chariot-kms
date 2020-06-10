import connexion


class RoutingInformation():
    '''
    class to handle both kafka topics and urls.
    
    When deserializing objects, this object keeps track of the path pointing to the resource / model.
    Transforms urls and kafka on the go.
    
    '''
    
    def __init__(self, base_url="", routing_url="", base_kafka="", routing_kafka=""):
        self.base_url = base_url
        self.routing_url = routing_url
        self.base_kafka = base_kafka
        self.routing_kafka = routing_kafka
        self.breadcrumbs_url = [base_url, ]
        self.breadcrumbs_kafka = [base_kafka, ]
    
    @staticmethod
    def create_root_routing_object():
        '''
        Build an empty routing object
        @return: A RoutingInformation object
        '''
        r = RoutingInformation(base_url=connexion.request.url_root + connexion.request.blueprint[1:] + "/",
                               routing_url=connexion.request.url,
                               base_kafka='kms.global.',
                               routing_kafka='')
        return r
    
    def add(self, crumb: str) -> None:
        '''
        add a crumb to the path to remember where the serializer has been
        @param crumb: a single string. Can contain multipart strings, e.g. /a/b/c
        @return: None
        '''
    
        self.breadcrumbs_url.append(crumb)
        self.breadcrumbs_kafka.append(crumb)

    def up(self) -> None:
        '''
        go back up in crumbs
        @return:
        '''
        try:
            self.breadcrumbs_url.pop()
            self.breadcrumbs_kafka.pop()
        except:
        
            pass

    def urlize(self, d: dict) -> None:
        '''
        Add this routinginformation object url and kafka to the dict.
        @param d: A dict to add the url and kafka topic to
        @return: None
        '''
        d['url'] = self._get_url()
        d['kafka_topic'] = self._get_kafka()

    def _get_url(self) -> str:
        '''
        Builds the url from breadcrumbs
        @return: Full url
        '''
        return "".join(self.breadcrumbs_url)

    def _get_kafka(self) -> str:
        '''
        Builds the kafka_topic from breadcrumbs
        @return: Full kafka_topic
        '''
        return "".join(self.breadcrumbs_kafka).replace("/", ".")

    def new_root(self, url: str, kafka: str) -> None:
        '''
        Rebase the root of routing to url and kafka_topic
        @param url: new url root
        @param kafka:  new kafka root
        @return: None
        '''
        self.base_url = url
        self.breadcrumbs_url = [url, ]
        self.base_kafka = kafka
        self.breadcrumbs_kafka = [kafka, ]
