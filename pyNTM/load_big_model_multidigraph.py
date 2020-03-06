from datetime import datetime
# import sys
# sys.path.append('../')

from pprint import pprint

from pyNTM import Parallel_Link_Model

time_before_load = datetime.now()

model = Parallel_Link_Model.load_model_file('big_model_multi_digraph_file.txt')

time_after_load = datetime.now()

model.update_simulation()

time_after_update_sim = datetime.now()

time_to_load = time_after_load - time_before_load
time_to_update_sim = time_after_update_sim - time_after_load

print("time_to_load = {}".format(time_to_load))
print("time_to_update_sim = {}".format(time_to_update_sim))

print("Ints over 100% util: "
      "{}".format(len([interface for interface in model.interface_objects if interface.utilization > 100])))

for interface in model.interface_objects:
    if interface.utilization > 100:
        print([interface.name, interface.node_object.name, interface.utilization])


