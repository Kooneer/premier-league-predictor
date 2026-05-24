import pandas as pd
import os
import yaml
from ingestion.fbref_provider import FBrefProvider

def main() -> None:
    # main.py localisation
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # config.yaml localisation
    config_path = os.path.join(base_dir, "config.yaml")

    with open(config_path, "r", encoding="utf-8") as f:
        config: dict = yaml.safe_load(f)

    league: str = config["provider"]["league"]
    target_season: str = config["provider"]["target_season"]
    historical_seasons: list[str] = config["provider"]["historical_seasons"]
    tmp = ["2023-2024","2022-2023"]

    provider = FBrefProvider(league=league)

    season_schedule: pd.DataFrame = provider.get_season_schedule(target_season)
    historical_schedules: pd.DataFrame = provider.get_seasons_schedules(historical_seasons)

    print(season_schedule.head())
    print(historical_schedules.head())


if __name__ == "__main__":
    main()