from opcua import Server
from random import randint
from opcua import ua
import datetime
import time

server = Server()

url = "opc.tcp://172.20.96.66:4840"                                                                                      #raspberry pi as server to write in KUKA cloud
server.set_endpoint(url)

name = "OPCUA_manual_server"
addspace = server.register_namespace(name)

node = server.get_objects_node()

SeverInfo = node.add_object(addspace, "OPCUA Simulation Server")
param = node.add_object(addspace, "Parameter")

Weight_actual = param.add_variable(addspace, "Single__set_Brick", 0)                                                     #digital weight
Weight_low_exp = param.add_variable(addspace, "min_weight_s_exp", 0)                                                     #min expected weight
Weight_high_exp = param.add_variable(addspace, "max_weight_s_exp", 0)                                                     #max expected weight
Bricks_value = param.add_variable(addspace, "Brick_ID", 0)                                                               #brick id
Quantities_value = param.add_variable(addspace, "Quantities", 0)                                                         #quantity number
    
Weight_actual.set_writable()
Weight_low_exp.set_writable()
Weight_high_exp.set_writable()
Bricks_value.set_writable()
Quantities_value.set_writable()

server.start()

def runserver_s(a, b, c, d, e):
    


    #--------

    actual_weight = a 
    min_weight = b 
    max_weight = c
    brick_id = d
    quantity_no = e
    
    print(actual_weight, min_weight, max_weight)
        
    Weight_actual.set_value(actual_weight)
    Weight_low_exp.set_value(min_weight)
    Weight_high_exp.set_value(max_weight)
    Bricks_value.set_value(brick_id)
    Quantities_value.set_value(quantity_no)
    
        
    time.sleep(2)

