# Pseudocode RBS FSM
from enum import Enum, auto
class State(Enum):
    S0 = auto()
    S1 = auto()
    S2 = auto()
    S3 = auto()
    S4 = auto()

passwd = [3,6,8]

if fsm.state==State.S0 and fsm.signal == passwd[0]:
    fsm.state = State.S1
elif fsm.state == State.S1 and fsm.signal == passwd[1]:
    fsm.state = State.S2
elif fsm.state == State.S2 and fsm.signal == passwd[2]:
    fsm.state = State.S3
else:
    fsm.state = State.S0


# Forstår ikke helt hvordan vi gjør det med rules
