import json
import time

from elastic_transport import TransportError
from elasticsearch import Elasticsearch
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from esExportRpc.config.conf import ES_HOST, ES_PORT
from esExportRpc.core.aliOssOp import uploadFileToAliOss
from esExportRpc.exc.err import RpcError
from loguru import logger as log


def exportAndUploadAliOss(indexName, scrollSize=1000, scrollTime='10m', maxRowsPerSheet=1048576):
    """
    导出es单个索引的所有数据到Excel, 并将Excel文件上传到阿里云OSS
    :param maxRowsPerSheet: Excel的最大行数, 默认1048576
    :param indexName: es索引名称
    :param scrollSize: 每次获取的文档数量, 默认1000
    :param scrollTime: scroll持续时间, 默认10分钟
    :return:
    """
    try:
        # 连接到Elasticsearch
        es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
        if not es.indices.exists(index=indexName):
            raise RpcError(error=f"索引{indexName}不存在")

        # 查询所有文档
        body = {
            "query": {
                "match_all": {}
            }
        }
        response = es.search(index=indexName, body=body, scroll=scrollTime, size=scrollSize)
        if isinstance(response['hits']['total'], dict):
            scrollSize = response['hits']['total']['value']
        else:
            scrollSize = response['hits']['total']
        # 创建一个新的工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = 'Sheet1'

        # 存储所有数据
        allDataList = []

        # 开始滚动读取数据
        while scrollSize > 0:
            allDataList.extend(response['hits']['hits'])
            sid = response['_scroll_id']
            response = es.scroll(scroll_id=sid, scroll=scrollTime)
            scrollSize = len(response['hits']['hits'])

        # 提取_source部分的数据
        documents = [doc['_source'] for doc in allDataList]

        # 转换为DataFrame
        df = pd.DataFrame(documents)
        stamp = time.time()
        targetExcelName = f'{indexName}_{stamp}.xlsx'

        # 创建一个ExcelWriter对象
        with pd.ExcelWriter(targetExcelName, engine='openpyxl') as writer:
            # 将DataFrame分批写入多个工作表
            chunkSize = maxRowsPerSheet - 1
            for i, chunk in enumerate(pd.read_csv(df.to_csv(index=False), chunksize=chunkSize)):
                ws = wb.create_sheet(title=f'Sheet{i + 2}') if i > 0 else wb.active
                for r in dataframe_to_rows(chunk, index=False, header=(i == 0)):
                    ws.append(r)

        # 保存工作簿
        wb.save(targetExcelName)
        ossFileObjectURL = uploadFileToAliOss(targetExcelName)
        return json.dumps({"downloadUrl": ossFileObjectURL, "fileName": targetExcelName})
    except ConnectionError:
        raise RpcError(error=f"无法连接到 [{ES_HOST}:{ES_PORT}]")
    except TransportError:
        raise RpcError(error=f"Elasticsearch传输层错误")
    except Exception as e:
        log.error(e)
        raise RpcError(error="导出失败")
