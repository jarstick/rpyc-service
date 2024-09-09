
from rpyc import Service
from esExportRpc.service.esExportServiceImpl import exportAndUploadAliOss


class EsExportService(Service):
    ALIASES = ['es-export-service']

    def exportSingleIndexAll(self, indexName):
        """
        对外暴露的导出es单个索引接口
        :param indexName:
        :return:
        """
        return exportAndUploadAliOss(indexName)

