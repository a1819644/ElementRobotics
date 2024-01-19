
import json
import serial
import time
from prettytable import PrettyTable
import msvcrt
import re

def process_received_data(data):
    # Decode the received bytes to a string
    received_table_str = data.decode('utf-8')
    
    # Process the received table string (for now, just print it)
    print(f"Received table:\n{received_table_str} \n\n")

# command input function
def input_command(ser):
    
    while True:
        print("Available commands in Normal Mode \n")
        # Display the commands
        print("""
        Available commands in Normal Mode
        Command Short description
        N-Transmits one Part Number datagram
        I-Transmits one Serial Number datagram
        C-Transmits one Configuration datagram
        T-Transmits one Bias Trim Offset datagram
        E-Transmits one Extended Error Information datagram
        R-Resets the unit
        SERVICEMODE-Enters Service Mode
        UTILITYMODE-Enters Utility Mode
        \n""")
        
        # Take user input
        user_input = input("Enter a command: ").upper()

        # Process the user input
        if user_input in ['N', 'I', 'C', 'T', 'E', 'R', 'SERVICEMODE', 'UTILITYMODE']:
            print(f"Selected command: {user_input}")
            command = user_input
            encoded_command = command.encode('utf-8')
            ser.write(encoded_command)
            time.sleep(2)  # Wait for the data to be transmitted
            while ser.in_waiting >0:
                ser.reset_output_buffer()  # Optional: Clear the output buffer
                # Read the response from the serial port
                data_receive = ser.read(ser.in_waiting).decode('utf-8')
                print(data_receive, "\n\n")
                # Split the data using the table identifier            
                # Find the index of the table identifier
                table_index = data_receive.find('+------------------------------------------------------+------------+')
                
                # Display only the part before the table if the identifier is found
                if table_index != -1:
                    print("\nReceived data\n", data_receive[:table_index])
           
                # Search for the part number line using regular expression
                # print()
        #     part_number_match = re.search(r'Program is in Utility mode', data_receive)
            
        #     # Check if the match is found
        #     if part_number_match:
        #         part_number = part_number_match.group(1)
        #         print("Extracted Part Number:", part_number)
        # else:
        #     print("Invalid command. Please enter a valid command.") 



        print("To exit the Normal Mode, please type 'Q' ")
        # Take user input
        user_input_for_exit = input("Enter a command: ").upper()
        if user_input_for_exit in ['Q']:
            exit()
        





def main():
    port_name = 'COM10'
    baud_rate = 115200

    try:
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Serial port {port_name} opened successfully.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    try:
        while True:
            # Read the bytes from the serial port
            received_data = ser.read(4096)  # may need to adjust the buffer size later if there is any data reading occurs in future
            if received_data:
                process_received_data(received_data)
                #displaying the commands on the screen for the users
                input_command(ser)   
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        ser.close()
        print(f"Serial port {port_name} closed.")

if __name__ == "__main__":
    main()
