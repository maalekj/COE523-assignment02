from time import sleep
import rticonnextdds_connector as rti
from os import path as os_path

file_path = os_path.dirname(os_path.abspath(__file__))

with rti.open_connector(
    config_name="MyDomainParticipantLibrary::SensorDomainParticipant",
    url=os_path.join(file_path, "HealthCareProject.xml"),
) as connector:
    output = connector.get_output("VitalPublisher::SensorToServerTopicWriter")

    for i in range(1, 500):
        output.instance.set_number("heartRate", 55)
        output.write()
        print("Sent")
        sleep(5)
