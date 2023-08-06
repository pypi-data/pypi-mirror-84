# %%
from pydantic.types import DirectoryPath
from sshtunnel import open_tunnel
import pymysql
from operator import methodcaller
import pandas as pd
import requests
import toolz.curried as tz
from pathlib import Path
from typing import Literal
import sqlite3
from pydantic import (
    BaseSettings,
    SecretStr,
    PositiveInt,
    FilePath,
)
import logging

__all__ = ["query", "Query"]

# %%
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )


# %%
class Query(BaseSettings):
    domo_client_id: str
    domo_secret: SecretStr
    domo_dataset_id: str

    remote_host: str="localhost"
    remote_port: PositiveInt=3306

    jump_host: str
    jump_port: PositiveInt=22
    jump_username: str
    jump_pkey: FilePath
    jump_password: SecretStr

    server_host: str
    server_port: PositiveInt=22
    server_username: str
    server_pkey: str
    server_password: SecretStr

    db_host: str="localhost"
    db_name: str
    db_username: str
    db_password: SecretStr

    sqlite_dw: FilePath

    class Config:
        env_file=str(Path("~/.atek/query").expanduser())
        env_file_encoding="utf-8"
        secrets_dir=str(Path("~/.atek/secrets").expanduser())

    def __str__(self):
        settings = "".join([f'  {k} = {v!r},\n' for k, v in self.dict().items()])
        return f"\n{__class__.__name__}(\n{settings})"

    def mysql(self, sql: str) -> pd.DataFrame:
        with open_tunnel(
            ssh_address_or_host=(self.jump_host, self.jump_port),
            remote_bind_address=(self.remote_host, self.remote_port),
            ssh_pkey=str(self.jump_pkey),
            ssh_username=self.jump_username,
            ssh_password=self.jump_password.get_secret_value(),
            ) as jump:
            logging.debug(f"Connected to {self.jump_host}:{self.jump_port}")
            with open_tunnel(
                ssh_address_or_host=(self.server_host, self.server_port),
                remote_bind_address=(self.remote_host, self.remote_port),
                ssh_pkey=self.server_pkey,
                ssh_username=self.server_username,
                ssh_password=self.server_password.get_secret_value(),
                ) as server:
                logging.debug(f"Connected to {self.server_host}:{self.server_port}")
                db = pymysql.connect(
                    host=self.db_host,
                    db=self.db_name,
                    user=self.db_username,
                    password=self.db_password.get_secret_value(),
                    port=server.local_bind_port,
                )
                logging.debug(f"Connected to {self.db_host}:{self.db_name}")
                df = pd.read_sql("select current_user, current_timestamp", db)
                logging.debug("Executed query")
                return df

    def domo(self, sql: str) -> pd.DataFrame:
        auth = requests.auth.HTTPBasicAuth(
            self.domo_client_id,
            self.domo_secret.get_secret_value()
        )
        auth_url=(
            "https://api.domo.com/oauth/token?"
            "grant_type=client_credentials&scope=data"
        )
        auth_response = requests.get(auth_url, auth=auth)
        token = auth_response.json()["access_token"]
        logging.debug("Authentiated to DOMO instance")
        header = {"Authorization": f"bearer {token}"}
        base_url="https://api.domo.com/v1/datasets"
        query = {"sql": sql}
        url = (
            f"{base_url}/query/execute/{self.domo_dataset_id}"
            "?includeHeaders=true"
        )
        logging.debug("Executing query")
        results = requests.post(url, headers=header, json=query).json()
        logging.debug("Reading data into DataFrame")
        columns = results["columns"]
        rows = results["rows"]
        data = [
            dict(zip(columns, row))
            for row in rows
        ]
        df = pd.DataFrame.from_records(data)
        return df

    def sqlite(self, sql: str) -> pd.DataFrame:
        db = sqlite3.connect(self.sqlite_dw)
        logging.debug("Connected to {self.sqlite_dw}")
        db.row_factory = lambda cursor, row: {
            col[0]: row[idx]
            for idx, col in enumerate(cursor.description)
        }
        logging.debug("Executing query")
        data = db.execute(sql)
        df = pd.DataFrame.from_records(data)
        logging.debug("Executed query")
        return df

# print(Query())
# ptable = lambda df: print(df.to_markdown(tablefmt="fancy_grid"))
# mysql_sql = "select current_user, current_timestamp"
# domo_sql = "select TrackingNumber, OrderDate from table limit 1"
# sqlite_sql = "select sqlite_version() as version, date('now') as today"
# ptable(Query().mysql(mysql_sql))
# ptable(Query().domo(domo_sql))
# ptable(Query().sqlite(sqlite_sql))

@tz.curry
def query(method: Literal["mysql", "domo", "sqlite"], sql: str) -> pd.DataFrame:
    _query = methodcaller(method, sql)
    q = Query()
    return _query(q)

# ptable(query("mysql", mysql_sql))
# ptable(query("domo", domo_sql))
# ptable(query("sqlite", sqlite_sql))
# %%