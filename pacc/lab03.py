import httpx
from prefect import flow, serve

from prefect.blocks.notifications 

@flow(name="fetch_weather")
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp


if __name__ == "__main__":
    # lat: float = 38.9
    # lon: float = -77.0

    fetch_weather_1_deployment = fetch_weather.to_deployment(name="fetch_weather_1")
    fetch_weather_2_deployment = fetch_weather.to_deployment(name="fetch_weather_2")
    fetch_weather_3_deployment = fetch_weather.to_deployment(name="fetch_weather_3")

    serve(
        fetch_weather_1_deployment,
        fetch_weather_2_deployment,
        fetch_weather_3_deployment,
    )
