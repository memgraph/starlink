import logging
from gqlalchemy import Memgraph
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
from time import sleep


log = logging.getLogger(__name__)


def connect_to_memgraph(memgraph_ip, memgraph_port):
    memgraph = Memgraph(host=memgraph_ip, port=int(memgraph_port))
    while(True):
        try:
            if (memgraph._get_cached_connection().is_active()):
                return memgraph
        except:
            log.info("Memgraph probably isn't running.")
            sleep(1)


def get_admin_client(kafka_ip, kafka_port):
    retries = 30
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=kafka_ip + ':' + kafka_port,
                client_id="starlink-stream")
            return admin_client
        except NoBrokersAvailable:
            retries -= 1
            if not retries:
                raise
            log.info("Failed to connect to Kafka")
            sleep(1)


def run(memgraph, kafka_ip, kafka_port):
    admin_client = get_admin_client(kafka_ip, kafka_port)
    log.info("Connected to Kafka")

    topic_list = [
        NewTopic(
            name="satellite",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="city",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="visible_from",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="delete_visible_from",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="laser_link",
            num_partitions=1,
            replication_factor=1)]

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
        pass
    log.info("Created topics")

    try:
        memgraph.drop_database()
        log.info("Creating stream connections on Memgraph")
        memgraph.execute(
            "CREATE KAFKA STREAM satellite_stream TOPICS satellite TRANSFORM starlink.satellite")
        memgraph.execute("START STREAM satellite_stream")
        memgraph.execute(
            "CREATE KAFKA STREAM city_stream TOPICS city TRANSFORM starlink.city")
        memgraph.execute("START STREAM city_stream")
        memgraph.execute(
            "CREATE KAFKA STREAM visible_from_stream TOPICS visible_from TRANSFORM starlink.visible_from")
        memgraph.execute("START STREAM visible_from_stream")
        memgraph.execute(
            "CREATE KAFKA STREAM delete_visible_from_stream TOPICS delete_visible_from TRANSFORM starlink.delete_visible_from")
        memgraph.execute("START STREAM delete_visible_from_stream")
        memgraph.execute(
            "CREATE KAFKA STREAM laser_link_stream TOPICS laser_link TRANSFORM starlink.laser_link")
        memgraph.execute("START STREAM laser_link_stream")
    except Exception as e:
        log.info(f"Error on stream creation: {e}")
        pass
