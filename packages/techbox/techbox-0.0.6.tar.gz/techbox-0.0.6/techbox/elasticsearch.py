import json

from elasticsearch import Elasticsearch


class MiscConfig:

    conditions = {
        "conditions": {
            "max_age":   "1d",
            "max_docs":  1000,
            "max_size": "1gb"
            }
    }

class DefaultIndex:

    def __init__(self, es_host, name, conditions=None, mappings_file=None):
        """
        name (str): the name of the index (an alias will be created)
        conditions (dict): The conditions for rollover jobs
        """
        self.alias = name
        self.index = name + "-00001"
        self.alias_body = {"is_write_index": True}

        if mappings_file:
            with open(mappings_file, "r") as f:
                self.mappings = json.loads(f.read())
        else:
            self.mappings = {}

        if isinstance(conditions, dict):
            self.conditions = conditions
        else:
            self.conditions = MiscConfig.conditions

        self.es = Elasticsearch(es_host)

    def _create_index(self):
        self.es.indices.create(self.index)
        self.es.indices.put_alias(self.index, self.alias, body=self.alias_body)

    def _create_rollover_config(self):
        self.es.indices.rollover(alias=self.alias, body=self.conditions)

    def _create_index_template(self):
        """
        Mapping example
        {
          "properties": {
            "data": {
              "type": "flattened"
            },
            "status": {
              "type": "text",
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              }
            }
          }
        }
        """

        template_name = self.alias + "-template"
        index_patterns = f"{self.alias}*"


        template = dict(mappings=self.mappings, aliases={self.alias: {}})

        body = dict(index_patterns=index_patterns, template=template)

        self.es.indices.put_template(template_name, body=body)

    def create(self):
        self._create_index()
        self._create_index_template()
        self._create_rollover_config()
