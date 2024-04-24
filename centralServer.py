import random
import time
import rticonnextdds_connector as rti
from os import path as os_path
import os

file_path = os_path.dirname(os_path.abspath(__file__))


os.environ["subscribeIntoPatient"] = str(
    1
)  # This line is not needed in the sensor code but if it is not there the rti complain about the missing environment variable it read in the XML file

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
            # store the data in a file as dictionary per line
            with open("data.txt", "a") as f:
                f.write(str(sample.get_dictionary()) + "\n")

            print(sample.get_dictionary())

            # read the last data added to data.txt file and send it providers
            with open("data.txt", "r") as f:
                data = f.readlines()[-1]
                data = eval(data)
                output.instance.set_dictionary(data)
                output.write()
