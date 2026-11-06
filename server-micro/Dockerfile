FROM python:3.12-slim-bookworm

# Microsoft ODBC Driver 18 so pyodbc can reach Azure SQL
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl gnupg ca-certificates unixodbc \
 && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
 && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list -o /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# gRPC code from protos/projects.proto (not committed; see generate_protos.py)
RUN python generate_protos.py

# 8000 = REST (default command). 50051 = gRPC: run the same image with the
# command "python grpc_server.py" (Azure: second container app, HTTP/2 ingress).
EXPOSE 8000 50051

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
