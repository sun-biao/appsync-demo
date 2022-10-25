aws kafka describe-cluster --region us-west-2 --cluster-arn "arn:aws:kafka:us-west-2:240778039237:cluster/tickerkafka/1446881f-74eb-40c4-a932-0be20106e950-1"

bin/kafka-topics.sh --create --zookeeper "z-3.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181" --replication-factor 2 --partitions 2 --topic multipartition


bin/kafka-topics.sh --list --zookeeper "z-3.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181" 
bin/kafka-topics.sh --describe --zookeeper "z-3.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181"  --topic multipartition


./kafka-console-consumer.sh --bootstrap-server "b-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:9092,b-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:9092" --consumer.config client.properties --topic multipartition
 ./kafka-console-producer.sh --broker-list "b-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:9092,b-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:9092" --producer.config client.properties --topic multipartition
//修改retion period
./kafka-configs.sh --zookeeper "z-3.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181,z-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:2181"  --entity-type topics --alter --add-config retention.ms=1000 --entity-name multipartition