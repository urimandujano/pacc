"""
Create a deployment that uses a subflow.
Use GitHub or other git-repo-based code storage.
Don't forget to push your code!
Check out the prefect.yaml file.
Add a cron schedule.
Pause the schedule.
Stretch: Create a second deployment that uses run_deployment
Super stretch: Create a webhook and automation that runs a deployment in response to an event firing
"""


import httpx
from prefect import flow

from prefect.filesystems import GitHub

from prefect.deployments import Deployment


@flow
def subflow():
    return httpx.get("https://example.com")


@flow
def test_flow():
    res = subflow()
    print(res)


def load_or_create_github_block(name: str = "urimandujano-pacc") -> GitHub:
    try:
        block = GitHub.load(name)
    except ValueError:
        print("Creating new Github block")
        block = GitHub(repository="https://github.com/urimandujano/pacc")
        block.save(name)
    return block


def deploy_flow():
    deployment = Deployment.build_from_flow(
        version=1,
        flow=test_flow,
        name="pacc-test-flow",
        work_queue_name="pacc-work-queue",
        work_pool_name="pacc-work-pool",
        storage=load_or_create_github_block(),
        apply=True,
    )
    deployment.apply()


if __name__ == "__main__":
    test_flow()
