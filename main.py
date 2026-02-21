
import asyncio
from agents import RescueAgent, SensorAgent


async def main():
    rescue = RescueAgent("rescue@localhost", "password")
    sensor = SensorAgent("sensor@localhost", "password")

    await rescue.start()
    await sensor.start()
    print("Agents started")
    try:
        while True:
            await asyncio.sleep(5)
    
    except KeyboardInterrupt:
        print("Stopping agents...")
        await rescue.stop()
        await sensor.stop()
        print("Agents stopped")


if __name__ == "__main__":
    asyncio.run(main())