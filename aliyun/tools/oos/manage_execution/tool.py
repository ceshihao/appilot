import json
from langchain.agents.tools import BaseTool

from tools.base.tools import RequireApprovalTool
from aliyun.client import AliyunClient
from aliyun import context as aliyun_context


class StartInstanceTool(RequireApprovalTool):
    """Tool to get current project and environment context."""

    name = "start_instance"
    description = (
        "Start an Aliyun ECS instance."
        "Input should be an ECS instance id like "
        'Output OOS execution id'
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:
        instance_id = text

        template_name = 'ACS-ECS-BulkyStartInstances'
        parameters = ('{"OOSAssumeRole":"","targets":{"ResourceIds":["' + instance_id +
                      '"],"RegionId":"cn-hangzhou","Type":"ResourceIds"},"regionId":"cn-hangzhou"}')

        try:
            execution_id = self.aliyun_client.start_execution(
                template_name, parameters
            )
            context = aliyun_context.Context(execution_id=execution_id)
            aliyun_context.update_context(context)
        except Exception as e:
            raise e


class ListExecutionTool(BaseTool):
    """Tool to change project and environment context."""

    name = "list_execution"
    description = (
        "List latest execution information."
        "No Input."
    )
    aliyun_client: AliyunClient

    def _run(self) -> str:
        execution_id = aliyun_context.GLOBAL_CONTEXT.execution_id

        try:
            execution = self.aliyun_client.list_executions(
                execution_id
            )
            return json.dumps(execution)
        except Exception as e:
            raise e
