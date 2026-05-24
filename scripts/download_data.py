import os
import pandas as pd
from src.config_loader import load_config
from src.ingestion.fbref_provider import FBrefProvider

def run_ingestion() -> None:
    config = load_config()
    league: str = config["provider"]["league"]
    target_season: str = config["provider"]["target_season"]
    historical_seasons: list[str] = config["provider"]["historical_seasons"]
    provider = FBrefProvider(league=league)

    target_season_schedule: pd.DataFrame = provider.get_season_schedule(target_season)
    historical_schedules: pd.DataFrame = provider.get_seasons_schedules(historical_seasons)

    # Paths
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    output_dir = os.path.join(project_root, "data", "raw")
    target_path = os.path.join(output_dir, "target_season_schedule.csv")
    historical_path = os.path.join(output_dir, "historical_schedules.csv")
    
    # Save to CSV file
    target_season_schedule.to_csv(target_path, index=False)
    historical_schedules.to_csv(historical_path, index=False)
if __name__ == "__main__":
    run_ingestion()