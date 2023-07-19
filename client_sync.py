import socket
import timeit

HOST = "127.0.0.1"
PORTS = [65430, 65431, 65432]

def get_value(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"r")
        data = s.recv(1024)
        data_int = int.from_bytes(data, 'big')
        return data_int

def get_average():
    num_values = 5
    values = []

    for port in PORTS:
        for _ in range(num_values):
            value = get_value(HOST, port)
            values.append(value)
            print(value)

    # Calculate average 
    average = sum(values) / len(values)
    return average

if __name__ == "__main__":
    start_time = timeit.default_timer()
    average_with_sync = get_average()
    print(f"Synchronous Average: {average_with_sync}")
    end_time = timeit.default_timer()
    print(f"Time taken to do the task: {end_time - start_time:.6f} seconds")

