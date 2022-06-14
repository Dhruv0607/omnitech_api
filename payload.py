import settings
import requests

# ip = '169.254.65.49'

'''
This functions decides the parameter "param" to send to the packet_gen function
Arguments: command_type - used to identify type of command being passed
'''
def payload_calc(command_type):
    if command_type == "C":
        for d in settings.rgbw:
            red_val = format(d['red'], 'X')
            green_val = format(d['green'], 'x')
            blue_val = format(d['blue'], 'x')
            white_val = format(d['white'], 'x')
            red_val = red_val.zfill(2)
            green_val = green_val.zfill(2)
            blue_val = blue_val.zfill(2)
            white_val = white_val.zfill(2)
        param = red_val + green_val + blue_val + white_val
        packet_gen(param, command_type)


'''
This function generates the packet to be sent to the device and assigns the value to the global "settings.packet" variable
Arguments: param - parameter received from the payload_calc function depending on the type of command
           command - used to identify type of command being passed
'''
def packet_gen(param, command):
    settings.packet_init()
    param_new = payload_gen(param)
    command_to_hex = hex(ord(command))
    crc = crc_calc(command_to_hex, param_new, "4", "0")
    settings.packet = settings.packet + command + "0004" + param + crc[2:] + "%0d%0a"
    print(settings.packet)


'''
This function is used to calculate the payload value
Arguments: val - refers to the actual hex value of payload
Returns the added hex value that is to be sent in the packet
'''
def payload_gen(val):
    temp_list = [val[i:i+2] for i in range(0, len(val), 2)]
    hex_sum = hex(int(temp_list[0], 16) + int(temp_list[1], 16) + int(temp_list[2], 16) + int(temp_list[3], 16))
    return hex_sum

'''
This function is used to calculate the CRC value of a given payload
Arguments: command_val - represents command type being sent
           payload_val - parameter received depending on the type of command
           val - size of the payload
           debug_val - debug value, either 00 or 01
Returns the CRC value
'''
def crc_calc(command_val, param_val, val, debug_val):
    crc_val = hex(int(command_val, 16) + int(param_val, 16) + int(val, 16) + int(debug_val, 16))
    print(hex(~int(crc_val, 16) & 0xffff))
    return hex(~int(crc_val, 16) & 0xffff)



'''
This functions sends the command request to specified "ip" and "packet"
'''
# def send_command_req():
#     print(f"command to ip: {ip}")
#     response = requests.post(f"http://{ip}/command?BROADCAST={settings.packet}")
#     response.close()
#     if response.status_code == 202:
#         return True
#     else:
#         return False