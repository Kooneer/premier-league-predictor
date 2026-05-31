import os
import pandas as pd
from src.config_loader import load_config
from src.ingestion.fbref_provider import FBrefProvider
from src.infrastructure.database import save_to_db

def run_ingestion() -> None:
    config = load_config()
    league: str = config["provider"]["league"]
    target_season: str = config["provider"]["target_season"]
    historical_seasons: list[str] = config["provider"]["historical_seasons"]
    provider = FBrefProvider(league=league)

    target_season_schedule: pd.DataFrame = provider.get_season_schedule(target_season)
    historical_schedules: pd.DataFrame = provider.get_seasons_schedules(historical_seasons)
   
    # Save to DB
    save_to_db(target_season_schedule, "raw_target_season")
    save_to_db(historical_schedules, "raw_historical_schedules")
    print("Data saved to DB.")

if __name__ == "__main__":
    run_ingestion()