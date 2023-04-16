import time
from cyclonedds.core import Listener, Qos, Policy
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter
from cyclonedds.util import duration

from i11eperf import a128, ou, TDUnion_t, DP_t, G128_t, Loc_t



qos = Qos(
	Policy.Reliability.Reliable(max_blocking_time=duration(seconds=10)),
	Policy.ResourceLimits(max_samples=77101, max_instances=-1, max_samples_per_instance=-1),
	Policy.History.KeepAll
)

domain_participant = DomainParticipant(0)
topic = Topic(domain_participant, "Data", ou, qos=qos)

writer = DataWriter(domain_participant, topic)



pos1 = Loc_t(latitude = 51.0, longitude=-1.0)
dp1 = DP_t(location=pos1, imageName='ABC')
dp1_data_union = TDUnion_t(dPValue=dp1)
guid1 = G128_t(data1=1234, data2=5678, data3=1234, data4=5678)

i = 1
while i < 60:
	the_sample = ou(id=guid1, orxxxxxxxxId=guid1, opxxxxxxxId=guid1, crxxxxxId=guid1, 
	                crxxxxxxTime=4, rxxxxxxd=False, vxxxxxLxxxxId=guid1, label='barf', content=dp1_data_union)
	print("Publish")	
	writer.write(sample=the_sample)
	time.sleep(2)
	

