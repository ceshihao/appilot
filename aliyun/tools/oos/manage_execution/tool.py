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
        targets = {
            "RegionId": "cn-hangzhou",
            "Type": "ResourceIds",
            "ResourceIds": instance_ids
        }
        parameters = {
            "OOSAssumeRole": "",
            "targets": targets,
            "regionId": "cn-hangzhou"
        }

        try:
            execution_id = self.aliyun_client.start_execution(
                template_name, json.dumps(parameters)
            )
            aliyun_context.set_default(execution_id=execution_id)
            return execution_id
        except Exception as e:
            raise e

class StopInstanceTool(RequireApprovalTool):
    """Tool to get current project and environment context."""

    name = "stop_instance"
    description = (
        "停止阿里云ECS实例。"
        "输入json格式。包含InstanceIds，用户必须输入，是一个数组。"
        "输出OOS执行Id。"
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:

        template_name = 'ACS-ECS-BulkyStopInstances'
        data = json.loads(text)
        instance_ids = data.get("InstanceIds")
        targets = {
            "RegionId": "cn-hangzhou",
            "Type": "ResourceIds",
            "ResourceIds": instance_ids
        }
        parameters = {
            "OOSAssumeRole": "",
            "targets": targets,
            "regionId": "cn-hangzhou"
        }

        try:
            execution_id = self.aliyun_client.start_execution(
                template_name, json.dumps(parameters)
            )
            aliyun_context.set_default(execution_id=execution_id)
            return execution_id
        except Exception as e:
            raise e


class ListExecutionTool(BaseTool):
    """Tool to change project and environment context."""

    name = "list_execution"
    description = (
        "查询OOS执行信息。"
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


class DescribeInstanceTool(BaseTool):
    """Tool to change project and environment context."""

    name = "describe_instance"
    description = (
        "查询ECS实例的相关属性信息。"
        "输入json格式。包含ECS实例ID InstanceId，用户必须输入，是一个字符串。如果没有提供输入可以反问。"
        "输出ECS实例的所有信息。"
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:
        # execution_id = aliyun_context.GLOBAL_CONTEXT.execution_id
        data = json.loads(text)
        instance_id = data.get("InstanceId")

        try:
            instance = self.aliyun_client.describe_instances(
                instance_id
            )
            return json.dumps(instance.to_map())
        except Exception as e:
            raise e


class DescribeImageTool(BaseTool):
    """Tool to change project and environment context."""

    name = "describe_image"
    description = (
        "查询ECS镜像的相关属性信息。"
        "输入json格式。包含ECS镜像ID ImageId，用户必须输入，是一个字符串。如果没有提供输入可以反问。"
        "输出ECS镜像的所有信息。"
    )
    aliyun_client: AliyunClient

    def _run(self, text: str) -> str:
        # execution_id = aliyun_context.GLOBAL_CONTEXT.execution_id
        data = json.loads(text)
        image_id = data.get("ImageId")

        try:
            image = self.aliyun_client.describe_images(
                image_id
            )
            return json.dumps(image.to_map())
        except Exception as e:
            raise e
