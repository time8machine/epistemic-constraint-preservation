import argparse,json,os
from .world import suite
from .agents import CollapseAgent,ROHAgent

def run(world,cls):
    a=cls(); rows=[]
    for o in world.stream:
        p=a.predict(o); a.update(o,p,o.actual)
        rows.append({"episode":o.episode,"prediction":p,"actual":o.actual,"error":int(p!=o.actual),"event":o.event,"affected":o.affected})
    return {"world_id":world.world_id,"family":world.family,"condition":a.condition,"rows":rows,"obstructions":a.obstruction_register if hasattr(a,"obstruction_register") else []}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--condition",choices=("collapse","roh","both"),default="both"); p.add_argument("--worlds",type=int,default=100); p.add_argument("--episodes",type=int,default=300); p.add_argument("--seed",type=int,default=10000); p.add_argument("--output",default="results"); x=p.parse_args()
    os.makedirs(x.output,exist_ok=True); worlds=suite(x.worlds,x.seed,x.episodes)
    classes={"collapse":CollapseAgent,"roh":ROHAgent}; cs=("collapse","roh") if x.condition=="both" else (x.condition,)
    for c in cs:
        with open(os.path.join(x.output,c+".json"),"w") as f: json.dump([run(w,classes[c]) for w in worlds],f)
if __name__=="__main__": main()
