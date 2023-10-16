from pydantic import BaseModel

from walrus.client import WalrusClient


class Context(BaseModel):
    execution_id: str = ""


GLOBAL_CONTEXT: Context


def set_default(
    execution_id: str = "",
) -> Context:

    global GLOBAL_CONTEXT
    GLOBAL_CONTEXT = Context(
        execution_id=execution_id
    )


def update_context(context):
    global GLOBAL_CONTEXT
    if context.get("execution_id") is not None:
        GLOBAL_CONTEXT.execution_id = context.get("execution_id")
