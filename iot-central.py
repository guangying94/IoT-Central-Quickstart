import Adafruit_DHT
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import Message
import json
import argparse

## Define arguement for scaling purpose
parser = argparse.ArgumentParser()
parser.add_argument("model_id", help="IoT Central Model ID")
parser.add_argument("id_scope", help="IoT Central ID Scope")
parser.add_argument("device_id", help="IoT Central Device ID")
parser.add_argument("device_key", help="IoT Central Device Key")
args = parser.parse_args()

model_id = args.model_id
id_scope = args.id_scope
registration_id = args.device_id
symmetric_key = args.device_key


## Function to establish connection with IoT Central
async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )
    provisioning_device_client.provisioning_payload = {"modelId": model_id}
    return await provisioning_device_client.register()

## Function to send message to IoT Central, wrap message as json
async def send_telemetry(device_client, telemetry_msg):
  msg = Message(json.dumps(telemetry_msg))
  msg.content_encoding = "utf-8"
  msg.content_type = "application/json"
  await device_client.send_message(msg)


## Main function to establish connection, and start sending message to IoT Central once connection is established.
## Run as a loop, sleep for 120 seconds
async def main():
  provisioning_host = "global.azure-devices-provisioning.net"

  registration_result = await provision_device(
    provisioning_host, id_scope, registration_id, symmetric_key, model_id
  )

  if registration_result.status == "assigned":
    print("Device was assigned")
    print(registration_result.registration_state.assigned_hub)
    print(registration_result.registration_state.device_id)

    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=symmetric_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id,
        product_info=model_id)
  else:
    raise RuntimeError(
      "Could not provision device. Aborting Plug and Play device connection."
    )

  await device_client.connect()

  while True:
    try:
      humidity, temperature = Adafruit_DHT.read_retry(11,21)

      if humidity is not None and temperature is not None:
        telemetry = {
          "Humidity": humidity,
          "Temperature": temperature
        }
        await send_telemetry(device_client, telemetry)

    except RuntimeError as error:
      print(error.args[0])

    except Exception as error:
      raise error
    await asyncio.sleep(120)

  await device_client.shutdown()

if __name__ == "__main__":
  asyncio.run(main())
