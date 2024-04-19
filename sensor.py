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
        "Please provide the patient ID as a parameter (e.g. python sensor.py <patient_id>)"
    )
    sys.exit(1)

patient_id = sys.argv[1]

os.environ["subscribeIntoPatient"] = str(
    patient_id
)  # This line is not needed in the sensor code but if it is not there the rti complain about the missing environment variable it read in the XML file

with rti.open_connector(
    config_name="MyDomainParticipantLibrary::SensorDomainParticipant",
    url=os_path.join(file_path, "HealthCareProject.xml"),
) as connector:
    output = connector.get_output("VitalPublisher::SensorToServerTopicWriter")

    for i in range(1, 500):
        # generate random data as simulation of real sensors.
        output.instance.set_number("patient_ID", int(patient_id))
        output.instance.set_number("heartRate", random.randint(40, 160))
        output.instance.set_number("bloodPressure", random.randint(60, 180))
        output.instance.set_number("oxygenSaturation", random.randint(60, 100))
        output.instance.set_number("timestamp", time.time())
        output.write()
        print("Sent")
        time.sleep(5)
