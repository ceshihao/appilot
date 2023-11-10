import json
from langchain.agents.tools import BaseTool

from tools.base.tools import RequireApprovalTool
from aliyun.client import AliyunClient
from aliyun import context as aliyun_context


class StartInstanceTool(RequireApprovalTool):
    """Tool to get current project and environment context."""

    name = "start_instance"
    description = (
        "启动阿里云ECS实例。"
        "输入json格式。包含InstanceIds，用户必须输入，是一个数组。"
        "输出OOS执行Id。"
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:

        template_name = 'ACS-ECS-BulkyStartInstances'
        data = json.loads(text)
        instance_ids = data.get("InstanceIds")
        print(instance_ids)
        targets = {
            "RegionId": "cn-hangzhou",
            "Type": "ResourceIds",
            "ResourceIds": instance_ids
        }
        print(targets)
        print(targets.get("ResourceIds"))
        parameters = {
            "OOSAssumeRole": "",
            "targets": targets,
            "regionId": "cn-hangzhou"
        }
        print(parameters)

        try:
            execution_id = self.aliyun_client.start_execution(
                template_name, json.dumps(parameters)
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
        "查询OOS执行信息"
        "输入json格式。包含ExecutionId，用户必须输入，是一个字符串。如果没有提供输入可以反问。"
        "输出OOS执行的所有信息。"
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:
        # execution_id = aliyun_context.GLOBAL_CONTEXT.execution_id
        data = json.loads(text)
        execution_id = data.get("ExecutionId")

        try:
            execution = self.aliyun_client.list_executions(
                execution_id
            )
            return json.dumps(execution.to_map())
        except Exception as e:
            raise e
