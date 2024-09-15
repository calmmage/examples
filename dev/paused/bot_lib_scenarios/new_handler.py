from bot_lib.handlers.handler import Handler
from enum import Enum

class State(Enum):
    Any = "any"
    Finish = "finish"

class NewHandler(Handler):

    # add ways to register state transitions. Optionally - extra filters and state Any and state Clear

    def register_state_transition(self, state_from: State, state_to: State, filter=None):
        if state_from is State.Any:
            self.router.message.register