try:
    from opcua import ua, uamethod, Server
    from opcua.server.user_manager import UserManager
    from time import sleep
except ImportError as e:
    print(e)

users_db =  {
                'user1': 'pw1'
            }

def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in users_db and password == users_db[username]

@uamethod
def myMethod(parent, rfid):
    print("method call with parameters: ", rfid)
    Out1 = rfid
    Out2 = 12345
    return  (
                ua.Variant(Out1, ua.VariantType.Int64),
                ua.Variant(Out2, ua.VariantType.Int64)
            )

if __name__ == "__main__":
    """
    OPC-UA-Server Setup
    """
    server = Server()

    endpoint = "opc.tcp://127.0.0.1:4840"
    server.set_endpoint(endpoint)

    servername = "Python-OPC-UA"
    server.set_server_name(servername)
    address_space = server.register_namespace(servername + "/namespace")
    
    uri = "urn:opcua:python:server"
    server.set_application_uri(uri)
    
    server.load_certificate("certificate.pem")
    server.load_private_key("key.pem")
    server.set_security_policy([
                                    # ua.SecurityPolicyType.NoSecurity,
                                    # ua.SecurityPolicyType.Basic128Rsa15_Sign,
                                    # ua.SecurityPolicyType.Basic128Rsa15_SignAndEncrypt,
                                    # ua.SecurityPolicyType.Basic256Sha256_Sign,
                                    ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt
                                ])
    policyIDs = ["Username"]
    server.set_security_IDs(policyIDs)
    server.user_manager.set_user_manager(user_manager)

    """
    OPC-UA-Modeling
    """
    root_node = server.get_root_node()
    object_node = server.get_objects_node()
    server_node = server.get_server_node()

    try:
        server.import_xml("custom_nodes.xml")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

    servicelevel_node = server.get_node("ns=0;i=2267") #Service-Level Node
    servicelevel_value = 255 #0-255 [Byte]
    servicelevel_dv = ua.DataValue(ua.Variant(servicelevel_value, ua.VariantType.Byte))
    servicelevel_node.set_value(servicelevel_dv)

    parameter_obj = server.nodes.objects.add_object(address_space, "Parameter")
    token_node = parameter_obj.add_variable(address_space, "token", ua.Variant(0, ua.VariantType.UInt32))
    token_node.set_writable() #if clients should be able to write

    myobj = server.nodes.objects.add_object(address_space, "Methods")
    multiply_node = myobj.add_method(   address_space, 
                                        "myMethod", 
                                        myMethod, 
                                        [
                                            #Input-Arguments:
                                            ua.VariantType.Int64
                                        ], 
                                        [
                                            #Output-Arguments:
                                            ua.VariantType.Int64,
                                            ua.VariantType.Int64
                                        ]
                                    )

    """
    OPC-UA-Server Start
    """
    server.start()

    try:
        while 1:
            sleep(1)
    except KeyboardInterrupt:
        server.stop()
