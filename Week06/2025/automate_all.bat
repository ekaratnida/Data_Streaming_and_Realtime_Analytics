@echo off
setlocal

echo ==========================================
echo Starting Kafka Infrastructure...
echo ==========================================
pushd kafka
docker-compose up -d
popd

echo.
echo ==========================================
echo Starting Sink Infrastructure...
echo ==========================================
pushd sink
docker-compose up -d
popd

echo.
echo ==========================================
echo Starting Source Infrastructure...
echo ==========================================
pushd source
docker-compose up -d
popd

echo.
echo Waiting for Kafka Connect to be ready (http://localhost:8083)...
echo This may take 30-60 seconds depending on your system.
timeout /t 45 /nobreak

echo.
echo ==========================================
echo Registering Sink Connector (sink2.json)...
echo ==========================================
curl -i -X POST -H "Content-Type: application/json" --data @sink/sink2.json http://localhost:8083/connectors

echo.
echo.
echo ==========================================
echo Registering Source Connector (source-timestamp-incrementing.json)...
echo ==========================================
curl -i -X POST -H "Content-Type: application/json" --data @source/source-timestamp-incrementing.json http://localhost:8083/connectors

echo.
echo.
echo ==========================================
echo Automation Script Completed!
echo ==========================================
pause
