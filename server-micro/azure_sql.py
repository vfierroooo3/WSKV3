"""Connection to the team's Azure SQL database (where ADF loads the city data).

Settings come from the environment (.env locally, app settings in Azure):
  AZURE_SQL_SERVER    e.g. myserver.database.windows.net
  AZURE_SQL_DATABASE  e.g. DMT_DB
  AZURE_SQL_USER / AZURE_SQL_PASSWORD
      SQL login for local runs. Leave both unset when deployed on Azure to
      sign in with the container's managed identity instead (no password).
"""
import os


def get_connection():
    import pyodbc  # imported here so the rest of the app still starts without the driver

    server = os.environ["AZURE_SQL_SERVER"]
    database = os.environ["AZURE_SQL_DATABASE"]
    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{server},1433;Database={database};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    user = os.environ.get("AZURE_SQL_USER")
    if user:
        conn_str += f"Uid={user};Pwd={os.environ.get('AZURE_SQL_PASSWORD', '')};"
    else:
        conn_str += "Authentication=ActiveDirectoryMsi;"
    return pyodbc.connect(conn_str)
