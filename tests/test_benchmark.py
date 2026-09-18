from roh.world import suite,rule_value

def test_100_worlds():
    ws=suite(100,10000,300)
    assert len(ws)==100
    assert [sum(w.family==f for w in ws) for f in ("threshold","parity","conjunction","relational","piecewise")]==[20]*5

def test_obstruction_events():
    w=suite(1,10000,300)[0]
    assert [o.episode for o in w.stream if o.event=="obstruction"]==[82,83,84,85,86]

def test_rules_differ():
    for w in suite(100,10000,300):
        assert any(rule_value(w.pre_rule,o.state,o.action)!=rule_value(w.post_rule,o.state,o.action) for o in w.stream)
