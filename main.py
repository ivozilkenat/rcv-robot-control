from core.sim import Simulation
from controller import Controller

if __name__ == "__main__":
    print("============================================================")
    print("IF OVERRIDE IS ENABLED, USE ARROW KEYS TO MOVE THE TRIANGLE")
    print("HOLD 'SPACE' TO RUN CONTROLLER")
    print("============================================================")

    simulation = Simulation(
        user_logic=Controller,
        allow_manuel_override=True
    )
    simulation.run()