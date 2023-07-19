import asyncio
import timeit


HOSTS = ["127.0.0.1"] * 3
PORTS = [65430, 65431, 65432]

async def get_value_async(host, port, num_values=10):
    values = []
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(b"r")

        for _ in range(num_values):
            data = await reader.read(1024)
            data_int = int.from_bytes(data, 'big')
            if data_int != 0:
                values.append(data_int)

            writer.close()
            await writer.wait_closed()
            reader, writer = await asyncio.open_connection(host, port)
            writer.write(b"r")

    except Exception as e:
        print(f"Error connecting to {host}:{port}: {e}")

    return values


async def async_main():
    num_values_per_server = 5 

    tasks = [get_value_async(HOSTS[i], PORTS[i], num_values_per_server) for i in range(len(HOSTS))]

    all_values = await asyncio.gather(*tasks)

    values = [value for values_per_server in all_values for value in values_per_server]

    # Calculate the sum
    total_sum = sum(values)

    # Calculate the average
    average = total_sum / (len(HOSTS) * num_values_per_server)

    return average
    

if __name__ == "__main__":
    start_time = timeit.default_timer()
    
    calculated_avarage = asyncio.run(async_main())
    print("Asynchronous Average:", calculated_avarage)

    end_time = timeit.default_timer()
    print(f"Time taken to retrieve all values: {end_time - start_time:.6f} seconds")
