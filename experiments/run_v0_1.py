import json, pathlib
from roh.world import suite
from roh.agents import CollapseAgent, ROHAgent

OUT=pathlib.Path("results/v0.1")

def run(world, cls):
    a=cls(); rows=[]
    for o in world.stream:
        p=a.predict(o); a.update(o,p,o.actual)
        rows.append({"episode":o.episode,"prediction":p,"actual":o.actual,"error":int(p!=o.actual),"event":o.event,"affected":o.affected})
    return {"world_id":world.world_id,"family":world.family,"condition":a.condition,"rows":rows,"obstructions":getattr(a,"obstruction_register",[])}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    worlds=suite(100,10000,300)
    (OUT/"worlds.json").write_text(json.dumps([{"world_id":w.world_id,"family":w.family,"pre_rule":w.pre_rule,"post_rule":w.post_rule,"change":w.change,"stream":[o.__dict__ for o in w.stream]} for w in worlds],indent=2))
    for cls in (CollapseAgent,ROHAgent):
        data=[run(w,cls) for w in worlds]
        (OUT/(cls.condition+".json")).write_text(json.dumps(data,indent=2))
    manifest={"benchmark":"ROH-Bench","version":"0.1","worlds":100,"episodes_per_world":300,"seed":10000,"conditions":["collapse","roh"],"status":"raw_run"}
    (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
