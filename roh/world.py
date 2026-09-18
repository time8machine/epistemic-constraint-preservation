from dataclasses import dataclass
import random

FAMILIES = ("threshold", "parity", "conjunction", "relational", "piecewise")
ACTIONS = 4
OUTCOMES = 4

@dataclass(frozen=True)
class Observation:
    episode: int
    state: tuple
    action: int
    actual: int
    phase: str
    event: str
    affected: bool

@dataclass
class World:
    world_id: int
    family: str
    pre_rule: dict
    post_rule: dict
    change: dict
    stream: list

def state(rng):
    return tuple([rng.randrange(2) for _ in range(6)] + [rng.randrange(3) for _ in range(2)])

def rule_value(rule, s, a):
    b=s[:6]; c=s[6:]
    f=rule["family"]
    if f=="threshold":
        z=sum(w*x for w,x in zip(rule["weights"],b))+rule["cw"]*c[0]+rule["aw"]*a
        return int(z>=rule["threshold"]) + (a%2)
    if f=="parity":
        z=rule["bias"]
        for i in rule["bits"]: z ^= b[i]
        if rule["use_action"]: z ^= a%2
        if rule["use_c0"]: z ^= c[0]%2
        return z%4
    if f=="conjunction":
        ok=all(b[i]==v for i,v in rule["b"].items()) and all(c[i]==v for i,v in rule["c"].items())
        if rule["action"] is not None: ok &= a==rule["action"]
        return rule["hit"] if ok else rule["miss"]
    if f=="relational":
        score=int(c[0]==c[1])+int(b[rule["i"]]==b[rule["j"]])+int(a==rule["action"])
        return (rule["base"]+score)%4
    if b[rule["gate"]]==rule["gate_value"]:
        return (rule["left_base"]+c[0]+a*rule["left_aw"])%4
    return (rule["right_base"]+b[rule["other"]]+c[1]*rule["right_cw"])%4

def pair(f,rng):
    if f=="threshold":
        pre={"family":f,"weights":[rng.choice((-2,-1,1,2)) for _ in range(6)],"cw":rng.choice((-2,-1,1,2)),"aw":rng.choice((-1,0,1)),"threshold":rng.randint(-1,4)}
        post={**pre,"weights":list(pre["weights"])}; i=rng.randrange(6); post["weights"][i]+=rng.choice((-2,-1,1,2))
        return pre,post,{"type":"coefficient_change","index":i}
    if f=="parity":
        bits=rng.sample(range(6),rng.randint(2,4))
        pre={"family":f,"bits":bits,"bias":rng.randrange(2),"use_action":rng.choice((True,False)),"use_c0":rng.choice((True,False))}
        post={**pre,"bits":list(bits)}; typ=rng.choice(("add_bit","toggle_action","toggle_c0"))
        if typ=="add_bit": post["bits"].append(next(i for i in range(6) if i not in bits))
        elif typ=="toggle_action": post["use_action"]=not pre["use_action"]
        else: post["use_c0"]=not pre["use_c0"]
        return pre,post,{"type":typ}
    if f=="conjunction":
        bi=rng.sample(range(6),rng.randint(2,3)); ci=rng.sample(range(2),rng.randint(0,1))
        pre={"family":f,"b":{i:rng.randrange(2) for i in bi},"c":{i:rng.randrange(3) for i in ci},"action":rng.choice((None,0,1,2,3)),"hit":rng.randrange(4),"miss":rng.randrange(4)}
        post={**pre,"b":dict(pre["b"]),"c":dict(pre["c"])}; typ=rng.choice(("b","c","action"))
        if typ=="b": i=rng.choice(bi); post["b"][i]=1-pre["b"][i]
        elif typ=="c" and ci: i=rng.choice(ci); post["c"][i]=(pre["c"][i]+1)%3
        else: post["action"]=0 if pre["action"] is None else (pre["action"]+1)%4
        return pre,post,{"type":"condition_change","target":typ}
    if f=="relational":
        i,j=rng.sample(range(6),2)
        pre={"family":f,"i":i,"j":j,"action":rng.randrange(4),"base":rng.randrange(4)}
        post={**pre}; field=rng.choice(("i","j","action")); post[field]=(pre[field]+1)%(6 if field!="action" else 4)
        return pre,post,{"type":"relation_change","field":field}
    pre={"family":f,"gate":rng.randrange(6),"gate_value":rng.randrange(2),"left_base":rng.randrange(4),"left_aw":rng.randrange(3),"right_base":rng.randrange(4),"other":rng.randrange(6),"right_cw":rng.randrange(3)}
    post={**pre}; field=rng.choice(("gate_value","left_aw","right_cw","other"))
    post[field]=(1-pre[field]) if field=="gate_value" else ((pre[field]+1)%3 if field in ("left_aw","right_cw") else (pre[field]+1)%6)
    return pre,post,{"type":"piece_change","field":field}

def generate_world(world_id,family,seed,episodes=300):
    rng=random.Random(seed); pre,post,change=pair(family,rng)
    changed=[]
    for _ in range(20000):
        s=state(rng); a=rng.randrange(ACTIONS)
        if rule_value(pre,s,a)!=rule_value(post,s,a): changed.append((s,a))
        if len(changed)>=30: break
    if len(changed)<5: raise RuntimeError("insufficient changed contexts")
    rng.shuffle(changed); stream=[]
    for t in range(1,episodes+1):
        if t<=80: phase="learn"
        elif t<=120: phase="obstruction"
        elif t<=180: phase="adaptation"
        elif t<=240: phase="stability"
        else: phase="transfer"
        if phase=="learn":
            s=state(rng); a=rng.randrange(4); y=rule_value(pre,s,a); event="ordinary"; affected=False
        elif phase=="obstruction" and 82<=t<=86:
            s,a=changed[t-82]; y=rule_value(post,s,a); event="obstruction"; affected=True
        elif phase=="obstruction" and t in (90,104,116):
            s=state(rng); a=rng.randrange(4); y=(rule_value(pre,s,a)+1+rng.randrange(3))%4; event="noise"; affected=False
        elif phase=="obstruction":
            s=state(rng); a=rng.randrange(4); y=rule_value(pre,s,a); event="ordinary"; affected=False
        elif phase=="stability" and t%2==0:
            s=state(rng); a=rng.randrange(4); y=rule_value(pre,s,a); event="old_rule_probe"; affected=False
        else:
            s=state(rng); a=rng.randrange(4); y=rule_value(post,s,a); event="transfer" if phase=="transfer" else "ordinary_post"; affected=rule_value(pre,s,a)!=y
        stream.append(Observation(t,s,a,y,"pre" if t<=120 else "post",event,affected))
    return World(world_id,family,pre,post,change,stream)

def suite(n=100,seed=10000,episodes=300):
    return [generate_world(i,FAMILIES[i//20],seed+i,episodes) for i in range(n)]
