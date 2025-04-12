import wmi

def get_device_specs():
    c = wmi.WMI()

    specs = {}

    for index ,cpu in enumerate(c.Win32_Processor()):
        specs[f"`CPU {index}`"] = f"{cpu.Name} | {cpu.ThreadCount} Cores"

    for index, gpu in enumerate(c.Win32_VideoController()):
        specs[f"`GPU {index}`"] = gpu.Name

    for index, ram in enumerate(c.Win32_PhysicalMemory()):
        specs[f"`RAM {index}`"] = f"{ram.PartNumber.strip()} by {ram.Manufacturer} | {float(ram.Capacity) / 1024 / 1024 / 1024:.1f}GB | Slot = {ram.BankLabel}"

    for index, disk in enumerate(c.Win32_DiskDrive()):
        is_usb = ""
        if disk.InterfaceType == "USB":
            is_usb = " `<- USB`"
        specs[f"`DISK {index}`"] = f"{disk.Caption} by {disk.Manufacturer} | {float(disk.Size) / 1024 / 1024 / 1024:.1f}GB{is_usb}"

    ignored_network_adapters = ["vpn", "virtual", "vm", "WAN Miniport", "Windscribe", "TunnelBear", "Debug"]

    real_network_index = 0
    for index, network_adapter in enumerate(c.Win32_NetworkAdapter()):
        ignored_flag = False
        for ignored in ignored_network_adapters:
            if ignored.lower() in network_adapter.Caption.lower() or ignored.lower() in network_adapter.Name.lower() or (network_adapter.MACAddress == None and network_adapter.NetConnectionID == None):
                ignored_flag = True

        if ignored_flag == False:
            specs[f"`NETWORK_ADAPTER {real_network_index}`"] = f"{network_adapter.Name} by {network_adapter.Manufacturer} | Using {network_adapter.NetConnectionID} | {network_adapter.MACAddress}"
            real_network_index += 1


    result = ""
    for spec, info in specs.items():
        result += f"{spec}: {info}\n"

    return result

def get_device_specs_raw():
    c = wmi.WMI()

    result = "Processors:- \n"

    for _ ,cpu in enumerate(c.Win32_Processor()):
        result += str(cpu)

    result += "\nVideo Controllers:- \n"

    for _, gpu in enumerate(c.Win32_VideoController()):
        result += str(gpu)

    result += "\nPhysical Memory:- \n"

    for _, ram in enumerate(c.Win32_PhysicalMemory()):
        result += str(ram)

    result += "\nDisk Drives:- \n"

    for _, disk in enumerate(c.Win32_DiskDrive()):
        result += str(disk)

    result += "\nNetwork Adapters:- \n"

    for _, network_adapter in enumerate(c.Win32_NetworkAdapter()):
        result += str(network_adapter)

    return result