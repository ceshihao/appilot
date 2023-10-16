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
        "Input should be an ECS instance id "
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
            # context = aliyun_context.set_default(execution_id=execution_id)
            # aliyun_context.update_context(context)
            return execution_id
        except Exception as e:
            raise e


class ListExecutionTool(BaseTool):
    """Tool to change project and environment context."""

    name = "list_execution"
    description = (
        "List latest execution information."
        "Input should be an OOS execution id."
        "Output OOS execution information."
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:
        # execution_id = aliyun_context.GLOBAL_CONTEXT.execution_id
        execution_id = text

        try:
            execution = self.aliyun_client.list_executions(
                execution_id
            )
            return json.dumps(execution.to_map())
        except Exception as e:
            raise e
