import logging

from langchain.schema.language_model import BaseLanguageModel

from aliyun.client import AliyunClient
from aliyun.tools.oos.manage_execution.tool import (StartInstanceTool, StopInstanceTool, ListExecutionTool,
                                                    DescribeInstanceTool, DescribeImageTool)

logger = logging.getLogger(__name__)


class AliyunToolKit:
    """Aliyun toolkit."""

    aliyun_client: AliyunClient
    llm: BaseLanguageModel

    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self.init_client()

    def init_client(self):
        self.aliyun_client = AliyunClient(
            access_key_id="",
            access_key_secret="",
            region_id="cn-hangzhou",
        )

    def get_tools(self):
        aliyun_client = self.aliyun_client
        llm = self.llm
        tools = [
            StartInstanceTool(aliyun_client=aliyun_client),
            StopInstanceTool(aliyun_client=aliyun_client),
            ListExecutionTool(aliyun_client=aliyun_client),
            DescribeInstanceTool(aliyun_client=aliyun_client),
            DescribeImageTool(aliyun_client=aliyun_client)
        ]
        return tools
