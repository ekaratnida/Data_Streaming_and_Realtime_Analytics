ARG CP_KAFKA_CONNECT_BASE_VERSION=7.2.2

FROM confluentinc/cp-kafka-connect-base:$CP_KAFKA_CONNECT_BASE_VERSION

ENV COMPONENT=kafka-connect
ENV CONNECT_PLUGIN_PATH=/usr/share/java,/usr/share/confluent-hub-components

#ARG CONFLUENTINC_JDBC_CONNECTOR_VERSION=10.5.4
#ARG CONFLUENTINC_HDFS_CONNECTOR_VERSION=10.1.13
#ARG CONFLUENTINC_ELASTICSEARCH_CONNECTOR_VERSION=14.0.2
#ARG CONFLUENTINC_S3_CONNECTOR_VERSION=10.2.2
#ARG CONFLUENTINC_AVRO_CONVERTER_CONNECTOR_VERSION=7.2.2
ARG JCUSTENBORDER_SPOOL_CONNECTOR_VERSION=2.0.64

RUN confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:$JCUSTENBORDER_SPOOL_CONNECTOR_VERSION

#RUN confluent-hub install --no-prompt confluentinc/kafka-connect-hdfs:$CONFLUENTINC_HDFS_CONNECTOR_VERSION \
#&& confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:$CONFLUENTINC_JDBC_CONNECTOR_VERSION \
#&& confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:$JCUSTENBORDER_SPOOL_CONNECTOR_VERSION \
#&& confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:$CONFLUENTINC_ELASTICSEARCH_CONNECTOR_VERSION \
#&& confluent-hub install --no-prompt confluentinc/kafka-connect-s3:$CONFLUENTINC_S3_CONNECTOR_VERSION \
#&& confluent-hub install --no-prompt confluentinc/kafka-connect-avro-converter:$CONFLUENTINC_AVRO_CONVERTER_CONNECTOR_VERSION