import asyncio
from spade.behaviour import FSMBehaviour, State

class RescueFSM(FSMBehaviour):
    async def on_start(self):
        print("FSM started")

class IdleState(State):
    async def run(self):
        print("State: IDLE")
        if self.agent.current_event:
            print("Event detected. Moving to ANALYZE.")
            self.set_next_state("ANALYZE")
        else:
            await asyncio.sleep(2)
            self.set_next_state("IDLE")

class AnalyzeState(State):
    async def run(self):
        print(f"STATE: ANALYZE | Event: {self.agent.current_event}")

        if self.agent.priority == 4:
            print("🔥 CRITICAL Emergency!")
        elif self.agent.priority == 3:
            print("⚠ High Priority")
        elif self.agent.priority == 2:
            print("📋 Medium Priority")
        elif self.agent.priority == 1:
            print("ℹ Low Priority")
        else:
            print(f"❓ Unknown Priority: {self.agent.priority}")
            self.set_next_state("IDLE")
            self.agent.current_event = None

        if self.agent.current_event:
            self.set_next_state("RESPOND")
        

class RespondState(State):
    async def run(self):
        print(f"STATE: RESPOND | Handling {self.agent.current_event}")

        await asyncio.sleep(2)

        print("Response completed.\n")

        self.agent.current_event = None
        self.agent.priority = 0

        self.set_next_state("IDLE")

