from soccerdata import FBref
import pandas as pd

class FBrefProvider:
    def __init__(self, league: str) -> None:
        self._league: str = league

    @property
    def league(self) -> str:
        return self._league;

    def get_season_schedule(self, season: str) -> pd.DataFrame:
        print(f"DEBUG: Initializing FBref for season: {season}")
        try:
            fbref_client = FBref(leagues=[self._league], seasons=[season])
            print("DEBUG: Initialized, downloading data...")
            schedule_df: pd.DataFrame = fbref_client.read_schedule()
            print("DEBUG: Data download.")
            return schedule_df
        except Exception as e:
            print(f"WARNING: Cannot download {season} season data. Error: {e}")
            print("Returned empty DataFrame")
            return pd.DataFrame()
    
    def get_seasons_schedules(self, seasons: list) -> pd.DataFrame:
        all_schedules: list = []
        for season in seasons:
            schedule_df: pd.DataFrame = self.get_season_schedule(season)
            if not schedule_df.empty:
                all_schedules.append(schedule_df)
        
        if all_schedules:
            return pd.concat(all_schedules, ignore_index=True)
        else:
            print("Returned empty DataFrame")
            return pd.DataFrame()