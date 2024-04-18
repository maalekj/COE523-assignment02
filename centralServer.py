import random
import time
import rticonnextdds_connector as rti
from os import path as os_path

file_path = os_path.dirname(os_path.abspath(__file__))

with rti.open_connector(
    config_name="MyDomainParticipantLibrary::CentralServerDomainParticipant",
    url=os_path.join(file_path, "HealthCareProject.xml"),
) as connector:
    input = connector.get_input("NewDateSubscriber::SensorToServerTopicReader")
    output = connector.get_output("StoredDatePublisher::ServerToProvidersTopicWriter")

    print("Waiting for data...")

    while True:
        input.wait()  # Wait for data
        input.take()
        for sample in input.samples.valid_data_iter:
            # TODO: Implement the logic to store the data in the database or file
            print(sample.get_dictionary())
