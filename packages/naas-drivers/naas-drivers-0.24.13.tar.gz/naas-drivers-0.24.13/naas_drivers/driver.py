import pandas as pd


class ConnectDriver:

    connected = False

    def connect(self, *args, **kwargs):
        print("define it", *args, **kwargs)
        self.connected = True
        return self

    def check_connect(self):
        if not self.connected:
            raise ValueError("you should call connect first")


class InDriver(ConnectDriver):
    def convert_data_to_df(self, *args, **kwargs):
        return "Define it, it should return a Dataframe"

    def get(self, *args, **kwargs) -> pd.DataFrame:
        self.check_connect()
        print("define it", *args, **kwargs)
        return "Define it, it should return a Dataframe"


class OutDriver(ConnectDriver):
    def send(self, *args, **kwargs):
        self.check_connect()
        print("define it", *args, **kwargs)
        return "Define it, it should return a Dataframe"
