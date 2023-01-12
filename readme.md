# Azure IoT Central Quickstart
This is the code repository for medium article [Remote Monitoring Simplified — Azure IoT Central QuickStart](https://medium.com/@marcustee/remote-monitoring-simplified-azure-iot-central-quickstart-4cba6777e2c3).

## Setup
This code uses Adafruit library, follow the setup [here](https://www.raspberrypi-spy.co.uk/2017/09/dht11-temperature-and-humidity-sensor-raspberry-pi/).

Update the parameters (DTDL Model ID, ID Scope, Device ID and Primary key) accordingly under unit file, and store this unit file under __/lib/systemd/system__ folder. 

Then, refresh the systemctl daemon and enable this service.

```bash
sudo systemctl daemon-reload
sudo systemctl enable dht.service
```