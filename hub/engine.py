from elasticsearch import Elasticsearch

class ESearch(object):
    def __init__(self):
        self.esearch   = Elasticsearch()
        self.connected = self.esearch.ping()

    def search(self, query, indices = [ ], meta = [ ]):
        response = [ ]

        return response

def search(query, types = [ ], fields = [ ]):
    esearch = ESearch()
    results = esearch.search(
        query   = query,
        indices = types,
        meta    = fields
    )

    return results
    