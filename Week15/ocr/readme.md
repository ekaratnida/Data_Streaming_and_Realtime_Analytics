## Install connector
- docker-compose build connect
- docker-compose up -d
- curl -X POST -H "Content-Type: application/json" --data @source.json http://localhost:8083/connectors

## Start pyspark
- Create spark-stuff folder in your current working directory.
- docker run -it -p 8888:8888 -v C:\Users\AS-LAB1\realtime-2568\week15-ocr\spark-stuff:/home/jovyan jupyter/pyspark-notebook

## Option
- To delete the existing connector:
  - curl -X DELETE http://localhost:8083/connectors/png-source
- To list all existing connectors:
  - curl http://localhost:8083/connector-plugins

## Mistral ocr tutorial
- https://colab.research.google.com/drive/1yfBKPKOa-osaeQv4yiTnA2LNYB76wu7C
