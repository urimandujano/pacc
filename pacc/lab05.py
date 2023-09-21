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


if __name__ == "__main__":
    test_flow()
