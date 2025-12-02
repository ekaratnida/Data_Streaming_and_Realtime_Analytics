## Install connector
- docker-compose build connect
- curl -X POST -H "Content-Type: application/json" --data @source.json http://localhost:8083/connectors
- curl -X DELETE http://localhost:8083/connectors/png-source


## Mistral ocr tutorial
- https://colab.research.google.com/drive/1yfBKPKOa-osaeQv4yiTnA2LNYB76wu7C
