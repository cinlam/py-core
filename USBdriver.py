## @file
# @brief Code for USB device communication.
#
# Use a list of vendor IDs and product IDs to connect to USB devices one after another.
# This code demonstrates how to communicate with a USB device using the pyusb library.
# It finds the specified USB device, performs operations such as reading/writing data,
# and handles kernel driver attachment and detachment if necessary.
#
# @note Make sure to install the pyusb library before running this code.
#       You can install it using pip: `pip install pyusb`
#
# @note Replace the VENDOR_ID and PRODUCT_ID with the appropriate values for your USB device.

import usb.core
import usb.util
from Serial import CommunicationStateMachine

object = CommunicationStateMachine ()

def connect_usb_device(serial_number):
    ## @brief Define a dictionary of device serial numbers and corresponding vendor IDs and product IDs
    DEVICE_LIST = {
        "FT57H93N": (0x0403, 0x6014),  # Device 1
        # Add more devices as needed
    }

    # Check if the provided serial number exists in the device list
    if serial_number not in DEVICE_LIST:
        raise ValueError("Device not found.")

    # Get the vendor ID and product ID for the selected device
    vendor_id, product_id = DEVICE_LIST[serial_number]

    # Find the USB device based on the vendor ID and product ID
    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

    # Check if the device is found
    if device is None:
        raise ValueError("Device not found.")

    # Perform operations with the device, such as reading/writing data

    # Check if the kernel driver is active and detach it if required
    if device.is_kernel_driver_active(0):
        print("Device found.")
        device.detach_kernel_driver(0)

    # Claim the USB device interface
    usb.util.claim_interface(device, 0)

    # Perform read/write operations or any other required actions
    data = []
    object.send_packet(data)
    # Release the USB device interface
    usb.util.release_interface(device, 0)

    # Reattach the kernel driver to the USB device if required
    device.attach_kernel_driver(0)


#serial_number = input("Enter the serial number of the device: ")
#connect_usb_device(serial_number)

