#!/bin/bash
set -e

# Start SQL Server in background
/opt/mssql/bin/sqlservr &
MSSQL_PID=$!

# Wait for SQL Server to be ready
echo "Waiting for SQL Server to start..."
for i in {1..60}; do
    /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -Q "SELECT 1" &>/dev/null && break
    sleep 1
done

# Check if a marker database exists to avoid re-running init
DBEXISTS=$(/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM sys.databases WHERE name='QuotePOC'" -h -1 -W)

if [ "$DBEXISTS" -eq "0" ]; then
    echo "Initializing database..."
    /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -i /opt/init-schema.sql
    /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -i /opt/seed-data.sql
    echo "Database initialized."
else
    echo "Database already exists, skipping init."
fi

# Keep SQL Server running in foreground
wait $MSSQL_PID
