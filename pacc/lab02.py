import httpx
from prefect import flow, task

from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact

RETRY_N = 0


@task(name="markit!", cache_key_fn=task_input_hash)
def markit(temp: float):
    markdown = f"""# Hello
## Group 2!!!!
#### Result: {temp}
"""

    create_markdown_artifact(
        key="",
        markdown=markdown,
        description="",
    )


@task(name="display_results")
def display_results(lat: float, long: float, temp: float):
    print(f"The weather at {lat} {long} is {temp}")


@flow(name="fetch_weather", retries=2, retry_delay_seconds=10, persist_result=True)
def fetch_weather(lat: float, lon: float):
    global RETRY_N
    RETRY_N += 1

    if RETRY_N != 2:
        raise Exception("Failure on purpose")

    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C: {most_recent_temp} degrees")

    markit(most_recent_temp)
    markit(most_recent_temp)
    markit(most_recent_temp)
    markit(most_recent_temp)

    display_results(lat, lon, most_recent_temp)
    return most_recent_temp


if __name__ == "__main__":
    lat: float = 38.9
    lon: float = -77.0
    fetch_weather.serve("uriel-tests")
