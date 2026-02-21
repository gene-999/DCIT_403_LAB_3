import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from fsm import AnalyzeState, IdleState, RescueFSM, RespondState


class RescueAgent(Agent):

    async def setup(self):
        print("Rescue Agent started")

        self.current_event = None
        self.priority = 0

        fsm = RescueFSM()

        fsm.add_state(name="IDLE", state=IdleState(), initial=True)
        fsm.add_state(name="ANALYZE", state=AnalyzeState())
        fsm.add_state(name="RESPOND", state=RespondState())

        fsm.add_transition("IDLE", "ANALYZE")
        fsm.add_transition("IDLE", "IDLE")
        fsm.add_transition("ANALYZE", "IDLE")
        fsm.add_transition("ANALYZE", "RESPOND")
        fsm.add_transition("RESPOND", "IDLE")

        self.add_behaviour(fsm)
        self.add_behaviour(self.ReceiveAlertBehaviour())

    class ReceiveAlertBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                event = msg.body

                priority_map = {
                    "fire_detected": 3,
                    "injury_reported": 2,
                    "low_battery": 1,
                    "gas_leak_detected": 4,
                    "power_outage": 3,
                    "security_breach": 4,
                    "network_outage": 3,
                    "temperature_high": 2,
                    "maintenance_due": 1,
                    "info_event": 0,
                }
                self.agent.current_event = event
                self.agent.priority = priority_map.get(event, 0)

                print(f"[EVENT RECEIVED] {event} | Priority: {self.agent.priority}")


class SensorAgent(Agent):

    class SendAlertsBehaviour(OneShotBehaviour):
        async def run(self):
            events = [
                "fire_detected",
                "injury_reported",
                "low_battery",
                "gas_leak_detected",
                "power_outage",
                "security_breach",
                "network_outage",
                "temperature_high",
                "maintenance_due",
                "info_event",
            ]

            for event in events:
                msg = Message(to="rescue@localhost")
                msg.body = event
                await self.send(msg)

                print(f"[SENSOR] Sent event: {event}")
                await asyncio.sleep(3)

    async def setup(self):
        print("Sensor Agent started")
        self.add_behaviour(self.SendAlertsBehaviour())
