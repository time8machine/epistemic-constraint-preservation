import argparse,json,statistics,random

METRICS=("POCE","T90","OR","FOR","RR","TA","BR","ORT")

def summary(run):
    rows=run["rows"]; err={r["episode"]:r["error"] for r in rows}
    poce=sum(err[t] for t in range(121,181))/60
    ta=sum(1-err[t] for t in range(241,301))/60
    # OR: five designated obstruction events that are retained as register entries.
    designated={82,83,84,85,86}; retained={x["first_episode"] for x in run["obstructions"]}
    orate=len(designated & retained)/5
    # This v0.1 implementation does not expose noise labels in the register; FOR is therefore
    # conservatively reported as 0 only for the baseline and marked unavailable for ROH below.
    forate=None if run["condition"]=="roh" else 0.0
    affected=[r for r in rows if r["episode"]>=82 and r["affected"]]
    rr=sum(r["error"] for r in affected)/len(affected) if affected else 0.0
    old=[r for r in rows if 181<=r["episode"]<=240 and r["event"]=="old_rule_probe"]
    br=1-(sum(r["error"] for r in old)/len(old) if old else 0)
    t90=60
    for t in range(121,172):
        if sum(err[k] for k in range(t,t+10))<=1: t90=t-120; break
    ort=None
    return {"POCE":poce,"T90":t90,"OR":orate,"FOR":forate,"RR":rr,"TA":ta,"BR":br,"CM":None,"ORT":ort}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--collapse",required=True); p.add_argument("--roh",required=True); x=p.parse_args()
    c=json.load(open(x.collapse)); r=json.load(open(x.roh)); cs=[summary(z) for z in c]; rs=[summary(z) for z in r]
    d=[a["POCE"]-b["POCE"] for a,b in zip(cs,rs)]; observed=statistics.mean(d)
    rng=random.Random(20260918); ge=0; n=20000
    for _ in range(n):
        s=sum(v if rng.getrandbits(1) else -v for v in d)/len(d)
        ge += s>=observed
    pval=(ge+1)/(n+1)
    print(json.dumps({"primary":{"metric":"POCE","collapse_minus_roh_mean":observed,"paired_sign_flip_p":pval,"n_worlds":len(d)},"collapse_mean":statistics.mean(x["POCE"] for x in cs),"roh_mean":statistics.mean(x["POCE"] for x in rs)},indent=2))
if __name__=="__main__": main()
