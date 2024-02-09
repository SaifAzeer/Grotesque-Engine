
class States_machine:
    def __init__(self) -> None:
        self.currentState = None
        self.globalState  = None

    def update(self):
        if self.currentState:
            self.currentState.Execute()
        if self.globalState:
            self.globalState.Execute()

    def change_state(self,newState):
        self.currentState.Exit()
        self.currentState = newState
        self.currentState.Start()

    def change_global_state(self,newState):
        self.globalState.exit()
        self.globalState = newState
        self.globalState.start()

_stateMachine = States_machine()