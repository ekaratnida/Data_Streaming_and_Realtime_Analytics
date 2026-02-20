@echo off

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
timeout /t 60

echo "Creating Sink Connector..."
curl -X POST -H "Content-Type: application/json" --data @"C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\sink\sink2.json" http://localhost:8083/connectors

echo "Creating Source Connector..."
curl -X POST -H "Content-Type: application/json" --data @"C:\Users\Admin\project\Data_Streaming_and_Realtime_Analytics\Week06\2025\source\source-timestamp-incrementing.json" http://localhost:8083/connectors

echo "Pipeline setup complete."
pause
