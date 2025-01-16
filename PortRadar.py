import socket
from datetime import datetime

def network_scanner_one_ip_one_port():
    print("_" * 50)
    print("Scanning started at: " + str(datetime.now()))
    print("_" * 50)

    one_ip_one_port = input("\nSpecify Target IP and Port: ")

    try:
        parts = one_ip_one_port.split()

        if len(parts) != 3:
            raise ValueError("Invalid input format. Expected exactly three parts.")

        command, ip, port = parts

        if command.lower() != "portradar":
            raise ValueError("Invalid command. Please start with 'PortRadar'.")

        port = int(port)

    except ValueError as ve:
        print(f"Error: {ve}")
        print("Please use the format 'PortRadar <ip> <port>' :")
        return

    print(f"\nStarting scan on {ip} at port {port}...\n")
    start_time = datetime.now()

    print("PORT          STATE           SERVICE              VERSION")

    scan_port(ip, port)
    end_time = datetime.now()
    total_time = end_time - start_time

    print(f"\nPortRadar done: {ip} scanned in {total_time}\n")

def network_scanner_one_ip_multiple_ports():
    print("_" * 50)
    print("Scanning started at: " + str(datetime.now()))
    print("_" * 50)

    input_string = input("\nSpecify Target IP and Ports: ")

    try:
        parts = input_string.split()

        if len(parts) < 3:
            raise ValueError("Invalid input format. Expected at least three parts.")

        command, ip, *ports = parts

        if command.lower() != "portradar":
            raise ValueError("Invalid command. Please start with 'PortRadar'.")

        ports = [int(port) for port in ports]

    except ValueError as ve:
        print(f"Error: {ve}")
        print("Please enter the command in the format 'PortRadar <ip> <port> <port> <port>...<nport>' : ")
        return

    print(f"\nStarting scan on {ip} for ports {', '.join(map(str, ports))}...\n")
    start_time = datetime.now()

    print("PORT          STATE           SERVICE              VERSION")

    for port in ports:
        scan_port(ip, port)

    end_time = datetime.now()
    total_time = end_time - start_time

    print(f"\nPortRadar done: {ip} scanned in {total_time}\n")


def get_service_name(port, proto='tcp'):
    try:
        return socket.getservbyport(port, proto)
    except OSError:
        return 'Unknown'

def get_service_version(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        s.send(b'HEAD / HTTP/1.1\r\n\r\n')
        server_response = s.recv(1024).decode().strip()
        s.close()
        return server_response
    except Exception as e:
        return f"Unknown (Error: {e})"

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    port_response = s.connect_ex((ip, port))

    if port_response == 0:
        state = "open"
        service_name = get_service_name(port)
        service_version = get_service_version(ip, port)
        print(f"{port}/tcp       {state}           {service_name}      {service_version}")

    elif port_response == 11:
        state = "filtered"
        print(f"{port}/tcp       {state}")

    else:
        state = "closed"
        print(f"{port}/tcp       {state}")

    s.close()

def choose_mode():
    while True:
        print("\nPlease choose a scanning mode: \n")
        print("1. Scan a single IP and port")
        print("2. Scan a single IP and multiple ports")
        print("\n")

        mode_choice = input("Enter your choice (1-2): ")

        try:
            mode_choice = int(mode_choice)
            if mode_choice < 1 or mode_choice > 2:
                raise ValueError

            confirm_choice = input(f"You have chosen mode {mode_choice}. Do you want to proceed? (y/n): ")
            if confirm_choice.lower() == 'y':
                return mode_choice
        except ValueError:
            print("Invalid input. Please enter either 1 or 2.")

def main():
    while True:
        start_command = input("Type 'PortRadar' to start our tool: ")
        if start_command.lower() != "portradar":
            print("Invalid command. Please type 'PortRadar' to start our tool.")
            continue

        while True:
            mode = choose_mode()

            if mode == 1:
                network_scanner_one_ip_one_port()
            elif mode == 2:
                network_scanner_one_ip_multiple_ports()
            else:
                print(f"\nMode {mode} is not yet implemented. Please choose mode 1 or 2.")

            repeat_the_process = input("Do you want to perform another scan? (y/n): ")
            if repeat_the_process.lower() != 'y':
                break

        exit_the_tool = input("Do you want to exit the tool? (y/n): ")
        if exit_the_tool.lower() == 'y':
            break

main()
