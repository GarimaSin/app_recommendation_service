# PyFlink job: consumes from Kafka 'events' topic, computes simple per-agent rolling count,
# and writes aggregated features to Redis (via Redis sink) or to a Kafka 'features' topic.
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.typeinfo import Types
import json, os, time
def run():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(4)
    properties = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP', 'kafka:9092'), 'group.id': 'flink-feat'}
    deserialization = lambda x: json.loads(x.decode('utf-8'))
    consumer = FlinkKafkaConsumer(topics=['events'], properties=properties, deserialization_schema=None)
    # Note: For brevity the job is a template; production job should use process functions and keyed state
    # Here we outline structure; implement actual process functions in production
    ds = env.add_source(consumer)
    # map to (agent,1)
    ds = ds.map(lambda x: (x.get('agent_id'), 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
    # TODO: key by agent and do windowed sum -> write to features topic or Redis
    # Placeholder sink to features topic
    producer = FlinkKafkaProducer(topic='features', bootstrap_servers=properties['bootstrap.servers'])
    ds.add_sink(producer)
    env.execute('feature_aggregator')
if __name__=='__main__':
    run()
