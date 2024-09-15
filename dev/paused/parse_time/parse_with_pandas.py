import pandas as pd


def parse_time(time_str):
    ts = pd.Timestamp(time_str)
    return ts


if __name__ == "__main__":
    time_str = "22:50"
    ts = parse_time(time_str)
    print(ts)
