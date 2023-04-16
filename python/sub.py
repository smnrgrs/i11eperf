from cyclonedds.core import Listener, Qos, Policy
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import Subscriber, DataReader
from cyclonedds.util import duration

from i11eperf import a128, ou


# This is the subscriber in the Vehicle Demo. It publishes a randomly moving
# vehicle updated every 0.1-1.0 seconds randomly. The 'Vehicle' class was
# generated from the vehicle.idl file with `idlc -l py vehicle.idl`

class MyListener(Listener):
    def on_liveliness_changed(self, reader, status):
        print(">> Liveliness event")
    def on_data_available(self, reader):
        print(">> On Data available")
    def on_inconsistent_topic(self, reader, status):
        print(">> On inconsistent topic")
    def on_liveliness_lost(self, reader, status):
        print(">> Liveliness lost")


listener = MyListener()
#qos = Qos(
#	Policy.Reliability.Reliable(max_blocking_time=duration(seconds=10)),
#	Policy.ResourceLimits(max_samples=77101, max_instances=-1, max_samples_per_instance=-1),
#	Policy.History.KeepAll,
#	Policy.Durability.Volatile,
#	Policy.Ownership.Exclusive
#)

qos = Qos(
	Policy.Reliability.Reliable(max_blocking_time=duration(seconds=10)),
	Policy.ResourceLimits(max_samples=77101, max_instances=-1, max_samples_per_instance=-1),
	Policy.History.KeepAll
)

domain_participant = DomainParticipant(0)
topic = Topic(domain_participant, "Data", ou, qos=qos)
subscriber = Subscriber(domain_participant)
reader = DataReader(domain_participant, topic)#, listener=listener)


for sample in reader.take_iter(timeout=duration(seconds=20)):
    print(sample)
