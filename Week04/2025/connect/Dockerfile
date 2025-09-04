FROM confluentinc/cp-kafka-connect:5.2.2

ENV CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components"

RUN confluent-hub install --no-prompt debezium/debezium-connector-mysql:0.9.5 \
	&& confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:5.2.2