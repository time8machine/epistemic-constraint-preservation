class CollapseAgent:
    condition="collapse"
    def __init__(self):
        self.memory={}; self.model_version=0
    def predict(self,obs):
        return self.memory.get((obs.state,obs.action),0)
    def update(self,obs,pred,actual):
        if pred!=actual:
            self.memory[(obs.state,obs.action)]=actual
            self.model_version+=1

class ROHAgent(CollapseAgent):
    condition="roh"
    def __init__(self):
        super().__init__(); self.obstruction_register=[]; self.unresolved={}
    def update(self,obs,pred,actual):
        if pred!=actual:
            key=(obs.state,obs.action)
            if key not in self.unresolved:
                rec={"first_episode":obs.episode,"state":obs.state,"action":obs.action,"prediction":pred,"observation":actual,"count":0}
                self.unresolved[key]=rec; self.obstruction_register.append(rec)
            self.unresolved[key]["count"]+=1
            self.memory[key]=actual
            self.model_version+=1
