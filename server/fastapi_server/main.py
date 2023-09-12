# Import necessary libraries
import logging                      # For logging messages
import uvicorn                      # ASGI server for FastAPI
from fastapi import FastAPI         # FastAPI framework

import pymacnet                     # Custom module for MacCORSpoofing functionality
import pymacnet.maccorspoofer       # Submodule for MacCORSpoofing
import pymacnet.messages            # Submodule for message handling

# Create a logger for this module
_logger = logging.getLogger(__name__)

# Create an instance of FastAPI
app = FastAPI()

# Configuration for the testing interface
FAST_API_CONFIG = {
    "server_ip": "0.0.0.0",   # IP address of the API server
    "port": 9000,               # Port for messages
}

# Configuration for the Maccor Spoofer server
MACCOR_SPOOFER_CONFIG = {
    "server_ip": FAST_API_CONFIG['server_ip'],      # IP address of the Maccor Spoofer server
    "json_port": 7889,                              # Port for JSON messages
    "tcp_port": 7890,                               # Port for TCP messages
    "num_channels": 128                             # Number of channels
}

# Configuration for the testing interface
CYCLER_INTERFACE_CONFIG = {
    'server_ip': MACCOR_SPOOFER_CONFIG['server_ip'],        # IP of the server
    'json_msg_port': MACCOR_SPOOFER_CONFIG['json_port'],    # Port for JSON messages
    'bin_msg_port': MACCOR_SPOOFER_CONFIG['tcp_port'],      # Port for binary messages
    'msg_buffer_size_bytes': 4096                           # Size of the message buffer in bytes
}

# Define a route and its corresponding function
@app.get("/")
def read_system_info():
    # Create a CyclerInterface for testing
    _logger.info("Creating CyclerInterface instance...")
    cycler_interface = pymacnet.CyclerInterface(CYCLER_INTERFACE_CONFIG)

    # Read system information from the CyclerInterface
    _logger.info("Reading system information....")
    system_info = cycler_interface.read_system_info()

    return {f"{pymacnet.messages.rx_system_info_msg['result']}"}


# If you're running this script directly, start the server
def main():
    # Create an instance of the Maccor Spoofer using the configuration
    maccor_spoofer = pymacnet.maccorspoofer.MaccorSpoofer(
        MACCOR_SPOOFER_CONFIG)

    # Start the Maccor Spoofer server
    _logger.info("Starting server...")
    maccor_spoofer.start()

    # Create an instance of the server using the configuration
    uvicorn.run(
        app, host=FAST_API_CONFIG['server_ip'], port=FAST_API_CONFIG['port'])


if __name__ == "__main__":
    # Configure logging to display INFO-level messages
    logging.basicConfig(level=logging.INFO)

    # Run the main function when the script is executed
    main()
