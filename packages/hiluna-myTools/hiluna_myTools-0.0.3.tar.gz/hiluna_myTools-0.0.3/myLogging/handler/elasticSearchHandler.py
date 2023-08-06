import logging
import time
from elasticsearch import Elasticsearch


class CustomHandler(logging.Handler):
    def __init__(self, host, user, password, index, port=9200, timeout=20):
        logging.Handler.__init__(self)
        self.es = Elasticsearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=(user, password),
            timeout=timeout
        )
        self.index = index
        mappings = {
            "mappings": {
                "properties": {
                    "id": {
                        "type": "long",
                        # "index": False
                    },
                    "msg": {
                        "type": "text",  # text不会进行分词,text会分词
                        # "index": False  # 不建索引
                    },
                    "filename": {
                        "type": "text",
                        # "index": False
                    },
                    "levelName": {
                        "type": "text",
                        # "index": False
                    },
                    "funcName": {
                        "type": "text",
                        # "index": False
                    },
                    "lineNum": {
                        "type": "long",
                        # "index": False
                    },
                    "process": {
                        "type": "long",
                        # "index": False
                    },
                    "processName": {
                        "type": "text",
                        # "index": False
                    },
                    "thread": {
                        "type": "long",
                        # "index": False
                    },
                    "threadName": {
                        "type": "text",
                        # "index": False
                    },
                    "time": {
                        "type": "date",
                    },
                }
            }
        }
        if not self.es.indices.exists(index=self.index):
            indexResult = self.es.indices.create(index=self.index, body=mappings)

    def emit(self, record):
        '''
        重写emit方法，这里主要是为了把初始化时的baseParam添加进来
        :param record:
        :return:
        '''

        data = {
            "id": str(record.created).replace(".", ""),
            "time": int(time.time()*1000),
            "msg": record.msg,
            "filename": record.filename,
            "levelName": record.levelname,
            "funcName": record.funcName.lower(),
            "lineNum": record.lineno,
            "process": record.process,
            "processName": record.processName,
            "thread": record.thread,
            "threadName": record.threadName,
        }

        try:
            self.es.index(index=self.index,  body=data)
        except Exception as e:
            pass
