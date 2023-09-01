import logging
from utils import utils
import urllib3

from walrus.client import WalrusClient

from pydantic import BaseModel
from dotenv import load_dotenv


class Context(BaseModel):
    project_id: str = ""
    project_name: str = ""
    environment_id: str = ""
    environment_name: str = ""


class Config(BaseModel):
    openai_api_key: str
    openai_api_base: str
    walrus_api_key: str
    walrus_url: str
    natural_language: str
    show_reasoning: bool
    verbose: bool
    skip_tls_verify: bool
    context: Context


CONFIG: Config


def init():
    load_dotenv()
    openai_api_base = utils.get_env("OPENAI_API_BASE")
    openai_api_key = utils.get_env("OPENAI_API_KEY")
    walrus_api_key = utils.get_env("WALRUS_API_KEY")
    walrus_url = utils.get_env("WALRUS_URL")
    walrus_default_project = utils.get_env("WALRUS_DEFAULT_PROJECT")
    walrus_default_environment = utils.get_env("WALRUS_DEFAULT_ENVIRONMENT")
    natural_language = utils.get_env("NATURAL_LANGUAGE", "English")
    show_reasoning = utils.get_env_bool("SHOW_REASONING", True)
    verbose = utils.get_env_bool("VERBOSE", False)
    skip_tls_verify = utils.get_env_bool("SKIP_TLS_VERIFY", False)

    if skip_tls_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if not walrus_url:
        raise Exception("WALRUS_URL is not set")
    if not walrus_api_key:
        raise Exception("WALRUS_API_KEY is not set")
    if not openai_api_key:
        raise Exception("OPENAI_API_KEY is not set")

    if not verbose:
        logging.basicConfig(level=logging.CRITICAL)

    global CONFIG
    context = _default_context(
        walrus_url,
        walrus_api_key,
        walrus_default_project,
        walrus_default_environment,
    )
    CONFIG = Config(
        openai_api_base=openai_api_base,
        openai_api_key=openai_api_key,
        walrus_api_key=walrus_api_key,
        walrus_url=walrus_url,
        natural_language=natural_language,
        show_reasoning=show_reasoning,
        verbose=verbose,
        skip_tls_verify=skip_tls_verify,
        context=context,
    )


def set_verbose(verbose: bool):
    global CONFIG
    CONFIG.verbose = verbose


def set_show_reasoning(show_reasoning: bool):
    global CONFIG
    CONFIG.show_reasoning = show_reasoning


def update_context(context):
    global CONFIG
    if (
        context.get("project_id") is not None
        and context.get("project_name") != ""
    ):
        CONFIG.context.project_id = context.get("project_id")
        CONFIG.context.project_name = context.get("project_name")
    if (
        context.get("environment_id") is not None
        and context.get("environment_name") != ""
    ):
        CONFIG.context.environment_id = context.get("environment_id")
        CONFIG.context.environment_name = context.get("environment_name")


def _default_context(
    walrus_url: str,
    walrus_api_key: str,
    default_project: str = "",
    default_environment: str = "",
) -> Context:
    walrus_client = WalrusClient(
        walrus_url,
        walrus_api_key,
        verify=False,
    )
    if default_project != "" and default_environment != "":
        project = walrus_client.get_project(default_project)
        environment = walrus_client.get_environment(
            default_project, default_environment
        )
    else:
        # Get the first project and environment if not specified.
        projects = walrus_client.list_projects()
        if projects is None or len(projects) == 0:
            raise Exception("No available project. A project is required.")
        project = projects[0]
        environments = walrus_client.list_environments(project.get("id"))
        if environments is None or len(environments) == 0:
            raise Exception(
                "No aviailable environment. An environment is required."
            )
        environment = environments[0]

    return Context(
        project_id=project.get("id"),
        project_name=project.get("name"),
        environment_id=environment.get("id"),
        environment_name=environment.get("name"),
    )
