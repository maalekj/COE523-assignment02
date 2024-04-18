import random
import time
import rticonnextdds_connector as rti
from os import path as os_path

file_path = os_path.dirname(os_path.abspath(__file__))

patient_id = 1  # TODO: Change this to the patient ID you got as parameter from the command line argument (like python sensor.py <patient_id>)

with rti.open_connector(
    config_name="MyDomainParticipantLibrary::SensorDomainParticipant",
    url=os_path.join(file_path, "HealthCareProject.xml"),
) as connector:
    output = connector.get_output("VitalPublisher::SensorToServerTopicWriter")

    for i in range(1, 500):
        output.instance.set_number("patient_ID", patient_id)
        output.instance.set_number("heartRate", random.randint(40, 160))
        output.instance.set_number("bloodPressure", random.randint(60, 180))
        output.instance.set_number("oxygenSaturation", random.randint(60, 100))
        output.instance.set_number("timestamp", time.time())
        output.write()
        print("Sent")
        time.sleep(5)
