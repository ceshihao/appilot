from alibabacloud_oos20190601.client import Client as OosClient
from alibabacloud_oos20190601.models import StartExecutionRequest, ListExecutionsRequest
from alibabacloud_tea_openapi.models import Config


class AliyunClient:
    """client for Aliyun API."""

    def __init__(self, access_key_id: str, access_key_secret: str, region_id: str, **kwargs):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region_id = region_id
        self.request_args = kwargs

    def start_execution(self, template_name: str, parameters: str):
        config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            region_id=self.region_id
        )
        client = OosClient(config)

        request = StartExecutionRequest(template_name=template_name, parameters=parameters)
        response = client.start_execution(request)
        return response.body.execution.execution_id

    def list_executions(self, execution_id: str):
        config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            region_id=self.region_id
        )
        client = OosClient(config)

        request = ListExecutionsRequest(execution_id=execution_id)
        response = client.list_executions(request)
        return response.body.executions[0]
