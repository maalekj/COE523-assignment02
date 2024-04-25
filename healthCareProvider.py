import random
import time
import rticonnextdds_connector as rti
from os import path as os_path
import os
import sys

file_path = os_path.dirname(os_path.abspath(__file__))

# check if the patient ID is provided as a parameter
if len(sys.argv) < 2:
    print(
        "Please provide the patient ID as a parameter (e.g. python healthCareProvider.py <patient_id>)"
    )
    sys.exit(1)

os.environ["subscribeIntoPatient"] = sys.argv[1]


with rti.open_connector(
    config_name="MyDomainParticipantLibrary::HealthCareProvider",
    url=os_path.join(file_path, "HealthCareProject.xml"),
) as connector:
    input = connector.get_input("StoredDateSubscriber::ServerToProvidersTopicReader")
    print("Waiting for data...")

    while True:
        input.wait()  # Wait for data
        input.take()
        for sample in input.samples.valid_data_iter:
            # print received data from the central server
            print(sample.get_dictionary())
