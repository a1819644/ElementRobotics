import serial
import time
from prettytable import PrettyTable # for displaying the status table
import random
import struct
import json

serial_mode_datagram_global = ""
part_number_datagram_global = ""
fw_config_global = ""

def simulate_stim300_data(serial_port):
    # For simplicity, let's send a sample datagram every second
          # Example: Generating a dummy datagram
            # Datagram content Identifier
            #     Rate 0x90
            #      0x91
            #     Rate and inclination 0x92
            #     Rate, acceleration and inclination 0x93
    # Table information
    table = PrettyTable()
    datagram_data = [
        ("Rate", 0x90),
        ("Rate and acceleration", 0x91),
        ("Rate and inclination", 0x92),
        ("Rate, acceleration and inclination", 0x93),
        ("Rate and temperature", 0x94),
        ("Rate, acceleration and temperature", 0xA5),
        ("Rate, inclination and temperature", 0xA6),
        ("Rate, acceleration, inclination and temperature", 0xA7),
        ("Rate and AUX", 0x98),
        ("Rate, acceleration and AUX", 0x99),
        ("Rate, inclination and AUX", 0x9A),
        ("Rate, acceleration, inclination and AUX", 0x9B),
        ("Rate, temperature and AUX", 0x9C),
        ("Rate, acceleration, temperature and AUX", 0xAD),
        ("Rate, inclination, temperature and AUX", 0xAE),
        ("Rate, acceleration, inclination, temperature and AUX", 0xAF),
    ]
    # Create a PrettyTable instance
    table = PrettyTable(["Datagram Content", "Identifier"])

    # Populate the table with data
    for row in datagram_data:
        table.add_row(row)

    # print(table)
    datagram = table.get_string().encode('utf-8')
    # send datagram
    serial_port.write(datagram)
    return table


#processing user input commands and requesting the transmission of the order data 
def switch(lang):
    global serial_mode_datagram_global, part_number_datagram_global, fw_config_global
    if lang == "N":
        # transmit a part number datagram (Im going to randomally alocate a part number)
        # Convert the part number to ASCII 
        ascii_part_number = convert_to_ascii(generate_random_part_number())
        part_number_datagram_global = ascii_part_number     
        return "Part Number datagram",ascii_part_number
    elif lang == "I":
        serial_number = generate_random_serial_number().hex().upper()
        serial_mode_datagram_global = serial_number
        return "Serial number Datagram",serial_number
    elif lang == "C":
        config_datagram = dummy_config_datagram()
        fw_config_global = config_datagram
        return "configuration Datagram", config_datagram
    elif lang == "T":
        bias_trim_offset_datagram = random_bias_trim_offset_datagram()
        return "bias Trim Offset Datagram", bias_trim_offset_datagram
    elif lang == "E":
        extended_error_datagram = random_extended_error_datagram()
        return "extended_error_datagram",extended_error_datagram
    elif lang == "R":
        rest_unit = reset_unit()
        if(rest_unit == True):
            return True
        else: 
            return False
    elif lang == "SERVICEMODE":
        Stim_data = service_mode(serial_mode_datagram_global, part_number_datagram_global, fw_config_global)
        return Stim_data
    elif lang == "UTILITYMODE":
        return utility_mode()

# follows the Table 5-14: Converting information in the Part Number datagram to ASCII 
def convert_to_ascii(part_number):
    ascii_result = ""
    for digit in part_number:
        value = int(digit, 16)  # Convert the hexadecimal digit to an integer

        if value < 10:
            ascii_result += chr(value + 48)
        else:
            ascii_result += chr(value + 55)

    return ascii_result

#generate random part number 
def generate_random_part_number():
    # Generate a random part number of the specified length
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(16))

# generate random serial number based on specification provided on the table:5-15
def generate_random_serial_number():
    # Generate random values for each digit (BCD) of the serial number
    serial_digits = [random.randint(0, 9) for _ in range(14)]

    # Generate the high and low nibbles for each digit
    serial_nibbles = [(digit // 10, digit % 10) for digit in serial_digits]

    # Combine the nibbles into bytes
    serial_bytes = [((high << 4) | low) for high, low in serial_nibbles]

    # Generate the Serial Number datagram identifier (0xB5 for datagrams without CR+LF termination)
    identifier = 0xB5

    # Generate the entire serial number datagram
    serial_number_datagram = bytes([identifier] + serial_bytes)

    return serial_number_datagram

# generate dummy config datagram base on the specification provided on table:5-16
def dummy_config_datagram():
    # Define configuration parameters
    config_byte_0 = 0b01111100  
    config_byte_1 = 0b01010101  
    config_byte_2 = 0b00110011  
    config_byte_3 = 0b11001100  
    config_byte_4 = 0b10101010  
    config_byte_5 = 0b00111100  
    config_byte_6 = 0b11010101  
    config_byte_7 = 0b10101010  
    config_byte_8 = 0b11110000  
    config_byte_9 = 0b01010101  
    config_byte_10 = 0b00110011  
    config_byte_11 = 0b11001100  
    config_byte_12 = 0b10101010  
    config_byte_13 = 0b00111100  
    config_byte_14 = 0b11010101  
    config_byte_15 = 0b10101010  

    # Pack the configuration data using the specified format as per table : 5-16
    configuration_data = struct.pack("<16B", config_byte_0, config_byte_1, config_byte_2,
                                     config_byte_3, config_byte_4, config_byte_5,
                                     config_byte_6, config_byte_7, config_byte_8,
                                     config_byte_9, config_byte_10, config_byte_11,
                                     config_byte_12, config_byte_13, config_byte_14,
                                     config_byte_15)

    return configuration_data

# generates dummy bias trim offset datagram on the specifcation provided on table: 5-17 
def random_bias_trim_offset_datagram():
    # Generate random values for each field
    identifier = random.choice([0xD1, 0xD2])
    gyro_bias_trim_offset_x = random.randint(0, 0xFFFF)
    gyro_bias_trim_offset_y = random.randint(0, 0xFFFF)
    gyro_bias_trim_offset_z = random.randint(0, 0xFFFF)
    accel_bias_trim_offset_x = random.randint(0, 0xFFFF)
    accel_bias_trim_offset_y = random.randint(0, 0xFFFF)
    accel_bias_trim_offset_z = random.randint(0, 0xFFFF)
    inclinometer_bias_trim_offset_x = random.randint(0, 0xFFFF)
    inclinometer_bias_trim_offset_y = random.randint(0, 0xFFFF)
    inclinometer_bias_trim_offset_z = random.randint(0, 0xFFFF)
    reference_info = random.randint(0, 0xFFFFFFFF)
    remaining_saves = random.randint(0, 0xFFFF)
    
    # Pack the data using the correct format of 20 items
    bias_trim_offset_datagram = struct.pack("<BHHHHHHHHHIHHHHHHHHI",
                                            identifier,
                                            gyro_bias_trim_offset_x, gyro_bias_trim_offset_y,
                                            gyro_bias_trim_offset_z, accel_bias_trim_offset_x,
                                            accel_bias_trim_offset_y, accel_bias_trim_offset_z,
                                            inclinometer_bias_trim_offset_x,
                                            inclinometer_bias_trim_offset_y,
                                            inclinometer_bias_trim_offset_z, reference_info,
                                            remaining_saves, 0, 0, 0, 0, 0, 0, 0, 0)
    
    return bias_trim_offset_datagram

# generate dummy rextended_error_datagram based on the specification provided on table : 5-18 
def random_extended_error_datagram():
    # Generate random values for each field
    identifier = random.choice([0xBE, 0xBF])
    # Generate random 128 bits for the Extended Error Information
    extended_error_info = random.getrandbits(128)
    identifier_bytes = bytes([identifier])
    extended_error_info_bytes = extended_error_info.to_bytes(16, byteorder='big')
    extended_error_datagram = identifier_bytes + extended_error_info_bytes
    
    return extended_error_datagram

# There is no description the reset the unit in handbook of SITM300
def reset_unit():
        # Add the implementation of the reset_unit function here
        return True

# Service mode
def service_mode(serial_number, part_number, fw_config):
    
    stim300_data = """
        SERIAL NUMBER = {serial_number}
        PRODUCT = STIM300
        PART NUMBER = {part_number}
        FW CONFIG = {fw_config}
        GYRO OUTPUT UNIT = [°/s] – ANGULAR RATE DELAYED
        ACCELEROMETER OUTPUT UNIT = [g] – ACCELERATION
        INCLINOMETER OUTPUT UNIT = [g] - ACCELERATION
        SAMPLE RATE [samples/s] = 2000
        GYRO CONFIG = XYZ
        ACCELEROMETER CONFIG = XYZ
        INCLINOMETER CONFIG = XYZ
        GYRO RANGE:
        X-AXIS: ± 400°/s
        Y-AXIS: ± 400°/s
        Z-AXIS: ± 400°/s
        ACCELEROMETER RANGE:
        X-AXIS: ± 10g
        Y-AXIS: ± 10g
        Z-AXIS: ± 10g
        INCLINOMETER RANGE:
        X-AXIS: ± 1.7g
        Y-AXIS: ± 1.7g
        Z-AXIS: ± 1.7g
        AUX RANGE: ± 2.5V
        GYRO LP FILTER -3dB FREQUENCY, X-AXIS [Hz] = 262
        GYRO LP FILTER -3dB FREQUENCY, Y-AXIS [Hz] = 262
        GYRO LP FILTER -3dB FREQUENCY, Z-AXIS [Hz] = 262
        ACCELEROMETER LP FILTER -3dB FREQUENCY, X-AXIS [Hz] = 262
        ACCELEROMETER LP FILTER -3dB FREQUENCY, Y-AXIS [Hz] = 262
        ACCELEROMETER LP FILTER -3dB FREQUENCY, Z-AXIS [Hz] = 262
        INCLINOMETER LP FILTER -3dB FREQUENCY, X-AXIS [Hz] = 262
        INCLINOMETER LP FILTER -3dB FREQUENCY, Y-AXIS [Hz] = 262
        INCLINOMETER LP FILTER -3dB FREQUENCY, Z-AXIS [Hz] = 262
        AUX LP FILTER -3dB FREQUENCY [Hz] = 262
        AUX COMP COEFF: A = 1.0000000e+00, B = 0.0000000e+00
        GYRO G-COMPENSATION:
        BIAS SOURCE, X-AXIS = OFF
        BIAS G-COMP LP-FILTER, X-AXIS = NA
        SCALE SOURCE, X-AXIS = ACC
        SCALE G-COMP LP-FILTER, X-AXIS = OFF
        BIAS SOURCE, Y-AXIS = OFF
        BIAS G-COMP LP-FILTER, Y-AXIS = NA
        SCALE SOURCE, Y-AXIS = ACC
        SCALE G-COMP LP-FILTER, Y-AXIS = OFF
        BIAS SOURCE, Z-AXIS = OFF
        BIAS G-COMP LP-FILTER, Z-AXIS = NA
        SCALE SOURCE, Z-AXIS = ACC
        SCALE G-COMP LP-FILTER, Z-AXIS = OFF
        G-COMP LP-FILTER CUTOFF = 0.010 HZ
        BIAS TRIM OFFSET:
        GYRO X-AXIS [°/s ] = 0.02343
        GYRO Y-AXIS [°/s ] = -0.01222
        GYRO Z-AXIS [°/s ] = 0.00111
        ACCELEROMETER X-AXIS [g ] = -0.004256
        ACCELEROMETER Y-AXIS [g ] = -0.013777
        ACCELEROMETER Z-AXIS [g ] = 0.000111
        INCLINOMETER X-AXIS [g ] = 0.0034256
        INCLINOMETER Y-AXIS [g ] = 0.0127598
        INCLINOMETER Z-AXIS [g ] = - 0.0005309
        REFERENCE INFO = 43639
        DATAGRAM = RATE, ACCELERATION, INCLINATION
        DATAGRAM TERMINATION = NONE
        BIT-RATE [bits/s] = 1843200
        DATA LENGTH = 8
        STOP BITS = 1
        PARITY = NONE
        LINE TERMINATION = ON
        SYSTEM CONFIGURATIONS:
        VOLTAGE-LEVEL OF DIGITAL OUTPUT SIGNALS: 5V
        TOV ACTIVE FOR SPECIAL DATAGRAMS AFTER POWER-ON/RESET: OFF
        BTO-DATAGRAM TRANSMISSION AFTER POWER-ON/RESET: OFF
        """
    return stim300_data

# Utility Mode
def utility_mode():
    return "ON"




def main():
 
    # virtual serial port
    port_name = 'COM9'  # Change this to your desired port
    baud_rate = 115200
    
    try:
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Serial port {port_name} opened successfully.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    try:
        while True:
            table = simulate_stim300_data(ser)
            # Check for incoming command from receiver
            while ser.in_waiting > 0:
                command_input_from_receiver = ser.readline().decode('utf-8')
                if command_input_from_receiver in ['N', 'I', 'C', 'T', 'E', 'R']:  # Example: 'R' for requesting data
                    # sending data to receiver
                    datagram_content,part_number = switch(command_input_from_receiver)
                    datagram_data = [datagram_content,part_number]
                    table.add_row(datagram_data) # needs to check this part
                    print(table)
                    amending_data = f"{datagram_content}:{part_number}"
                    print("\n", amending_data)
                    sending_data = amending_data.encode('utf-8') 
                    ser.write(sending_data)
                elif command_input_from_receiver in [ 'UTILITYMODE']:  # Example: 'R' for requesting data
                    # sending data to receiver
                    datagram_content = switch(command_input_from_receiver)
                    amending_data = f"Program is going into the utility mode :{datagram_content}"
                    print(datagram_content)
                    sending_data = datagram_content.encode('utf-8') 
                    ser.write(sending_data)
            time.sleep(1)


    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        ser.close()
        print(f"Serial port {port_name} closed.")


if __name__ == "__main__":
    main()
