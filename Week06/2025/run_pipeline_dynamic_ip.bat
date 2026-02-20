@echo off
SETLOCAL

REM Check for IP address argument
IF [%1]==[] (
    echo "Usage: %0 <ip_address>"
    GOTO :EOF
)

SET IP_ADDRESS=%1
SET SINK_CONFIG_IN=C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\sink\sink2.json
SET SOURCE_CONFIG_IN=C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\source\source-timestamp-incrementing.json
SET SINK_CONFIG_OUT=%TEMP%\sink2_temp.json
SET SOURCE_CONFIG_OUT=%TEMP%\source-timestamp-incrementing_temp.json

echo "Using IP address: %IP_ADDRESS%"

REM Replace IP in sink config
powershell -Command "(Get-Content -path '%SINK_CONFIG_IN%' -Raw) -replace '172.11.251.242', '%IP_ADDRESS%' | Set-Content -path '%SINK_CONFIG_OUT%'"

REM Replace IP in source config
powershell -Command "(Get-Content -path '%SOURCE_CONFIG_IN%' -Raw) -replace '172.11.251.242', '%IP_ADDRESS%' | Set-Content -path '%SOURCE_CONFIG_OUT%'"


echo "Starting Kafka..."
docker-compose -f C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\kafka\docker-compose.yml up -d
echo "Waiting for Kafka to start..."
timeout /t 30

echo "Starting Sink..."
docker-compose -f C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\sink\docker-compose.yml up -d
echo "Waiting for Sink to start..."
timeout /t 10

echo "Starting Source..."
docker-compose -f C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\source\docker-compose.yml up -d
echo "Waiting for Source to start..."
timeout /t 10

echo "Creating Sink Connector..."
curl -X POST -H "Content-Type: application/json" --data @"%SINK_CONFIG_OUT%" http://localhost:8083/connectors

echo "Creating Source Connector..."
curl -X POST -H "Content-Type: application/json" --data @"%SOURCE_CONFIG_OUT%" http://localhost:8083/connectors

echo "Cleaning up temporary files..."
del "%SINK_CONFIG_OUT%"
del "%SOURCE_CONFIG_OUT%"

echo "Pipeline setup complete."
pause
