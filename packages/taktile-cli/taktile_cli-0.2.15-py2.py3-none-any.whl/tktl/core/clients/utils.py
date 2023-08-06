from typing import Any, Callable, List

from pydantic import UUID4

from .. import loggers as sdk_logger
from ..schemas.repository import Endpoint, Repository, RepositoryDeployment
from ..t import Resources

_logger = sdk_logger.SdkLogger()

default_comp = lambda x, y: x == y


def filter_prop(
    resources: List[Resources], prop_name: str, value: Any, key: Callable = default_comp
):
    if value is not None:
        return [d for d in resources if key(value, getattr(d, prop_name))]
    return resources


def filter_empty_and_duplicate_resources(resources: List[Resources]):
    non_empty = [r for r in resources if r.id]
    # can't use set() since BaseModels are not hashable
    return [x for i, x in enumerate(non_empty) if i == non_empty.index(x)]


def filter_deployments(
    deployments: List[RepositoryDeployment],
    deployment_id: UUID4,
    commit_sha: str = None,
    branch_name: str = None,
    status_name: str = None,
) -> List[RepositoryDeployment]:
    if deployment_id:
        deployments = [d for d in deployments if d.id == deployment_id]

        if deployments:
            return deployments
        else:
            _logger.warning("No deployments with matching id found")

    for n, v in zip(
        ["commit_hash", "branch_name", "status"], [commit_sha, branch_name, status_name]
    ):
        if n == "commit_hash" and commit_sha:
            if len(commit_sha) < 40:
                comp = lambda x, y: y.startswith(x)
            else:
                comp = default_comp
        else:
            comp = default_comp
        deployments = filter_prop(deployments, prop_name=n, value=v, key=comp)

    return filter_empty_and_duplicate_resources(deployments)


def filter_repositories(
    repositories: List[Repository],
    repository_id: UUID4,
    repository_name: str = None,
    repository_owner: str = None,
) -> List[Repository]:
    if repository_id:
        repositories = [r for r in repositories if r.id == repository_id]
        if repositories:
            return repositories
        else:
            _logger.warning("No repositories with matching id found")

    for n, v in zip(
        ["repository_name", "repository_owner"], [repository_name, repository_owner]
    ):
        repositories = filter_prop(repositories, prop_name=n, value=v)
    return filter_empty_and_duplicate_resources(repositories)


def filter_endpoints(
    endpoints: List[Endpoint], endpoint_id: UUID4, endpoint_name: str = None
) -> List[Endpoint]:
    if endpoint_id:
        endpoints = [r for r in endpoints if r.id == endpoint_id]
        if endpoints:
            return endpoints
        else:
            _logger.warning("No endpoints with matching id found")

    for n, v in zip(["endpoint_name"], [endpoint_name]):
        endpoints = filter_prop(endpoints, prop_name=n, value=v)
    return filter_empty_and_duplicate_resources(endpoints)
