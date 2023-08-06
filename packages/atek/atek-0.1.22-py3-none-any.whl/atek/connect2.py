# %%
from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd
import requests
import toolz.curried as tz
from typing import Dict, Any, Optional, Tuple
from pydantic import (
    BaseSettings,
    SecretStr,
    PositiveInt,
    DirectoryPath,
    Field,
    HttpUrl,
)
import logging

__all__ = ["query", "Config"]

# %%
logging.basicConfig(
    level="INFO",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# %%
class Config(BaseSettings):
    directory: DirectoryPath = Field(...,env="ATEK_CACHE")

    def settings(self, *names: str) -> DirectoryPath:
        return self.directory.joinpath(*names)

    def server(self, *names: str) -> "Server":
        return Server(_env_file=self.settings(*names, "server"))

    def database(self, *names: str) -> "Database":
        return Database(_env_file=self.settings(*names, "database"))

    def domo(self, *names: str) -> "Domo":
        return Domo(_env_file=self.settings(*names, "domo"))

# Config().settings("public_html", "server")


# %%
class Server(BaseSettings):
    host: str
    port: PositiveInt=22
    remote_host: str="localhost"
    remote_port: PositiveInt=3306
    username: str
    pkey: str="${HOME}/.ssh/id_rsa"
    password: SecretStr

    @property
    def login(self) -> Dict[str,Any]:
        return {
            "ssh_address_or_host": (self.host, self.port),
            "remote_bind_address": (self.remote_host, self.remote_port),
            "ssh_username": self.username,
            "ssh_pkey": str(self.pkey),
            "ssh_password": self.password.get_secret_value(),
        }

# Server(_env_file=Config().settings("public_html", "server"))


# %%
class Database(BaseSettings):
    host: str="localhost"
    db: str
    username: str
    password: SecretStr

    @property
    def login(self) -> Dict[str,Any]:
        return {
            "host": self.host,
            "db": self.db,
            "user": self.username,
            "password": self.password.get_secret_value(),
        }

# Database(_env_file=Config().settings("public_html", "database"))


# %%
class Domo(BaseSettings):
    client_id: SecretStr
    secret: SecretStr
    base_url: HttpUrl
    auth_url: HttpUrl
    dataset_id: str

    @property
    def auth(self) -> Tuple[str,str]:
        return tuple([
            self.client_id.get_secret_value(),
            self.secret.get_secret_value()
        ])

# Domo(_env_file=Config().settings("domo_appraisal", "domo"))


# %%
def ssh_mysql(sql: str, *names: str, config: Optional[Config]=None
    ) -> pd.DataFrame:
    # Get the parameters to connect
    config = config or Config()
    server = config.server(*names)
    database = config.database(*names)

    # Connect to ssh server
    with SSHTunnelForwarder(**server.login) as tunnel:
        logging.info("SSH Tunnel established")
        # connect to MySQL database on ssh server
        try:
            db = pymysql.connect(**database.login, port=tunnel.local_bind_port)
            logging.info("Database connection established")
            logging.info("Query started")
            result = pd.read_sql(sql, db)
            db.close()
            logging.info("Query finished")
        except Exception:
            logging.error(server)
            logging.error(database)
            logging.error(sql)
            raise
    return result

# ssh_mysql("select current_user", "public_html")
# ssh_mysql("select current_user", "rs1")


# %%
def api_domo(sql: str, *names: str, config: Optional[Config]=None
    ) -> pd.DataFrame:
    # Get the parameters to connect
    config = config or Config()
    domo = config.domo(*names)

    # Authenticate
    try:
        auth = requests.auth.HTTPBasicAuth(*domo.auth)
        auth_response = requests.get(domo.auth_url, auth=auth)
        token = auth_response.json()["access_token"]
        logging.info("Authenticated")
    except:
        logging.error(config)
        logging.error(domo)
        raise

    # Create and return the authorization header
    header = {"Authorization": f"bearer {token}"}

    # Get the results of the query in json format
    try:
        query = {"sql": sql}
        url = f"{domo.base_url}/query/execute/{domo.dataset_id}?includeHeaders=true"
        logging.info("Query started")
        results = requests.post(url, headers=header, json=query).json()
        logging.info("Query finished")
    except:
        logging.error(f"{url=}")
        logging.error(f"{sql=}")
        raise

    # Create a list of dicts and pass into a dataframe
    logging.info("Converting results to list of dicts")
    columns = results["columns"]
    rows = results["rows"]
    data = [
        dict(zip(columns, row))
        for row in rows
    ]
    logging.info("Converting list of dicts to DataFrame")
    df = pd.DataFrame.from_records(data)
    logging.info("DataFrame created")
    return df
# api_domo("select TrackingNumber from table limit 1", "domo_appraisal")


# %%
@tz.curry
def query(source: str, sql: str) -> pd.DataFrame:
    logging.debug(f"{source=}")
    if source in ["public_html", "rs1"]:
        logging.debug("Dispatching to ssh_mysql")
        return ssh_mysql(sql, source)
    if source in ["domo_appraisal"]:
        logging.debug("Dispatching to api_domo")
        return api_domo(sql, source)

# query("public_html", "select current_user")
# tz.pipe("select current_user", query("public_html"), print)
# tz.pipe(
#     "select TrackingNumber, OrderDate from table limit 10"
#     ,query("domo_appraisal")
#     ,print
# )
# %%
