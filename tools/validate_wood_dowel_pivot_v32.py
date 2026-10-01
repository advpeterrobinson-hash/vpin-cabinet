"""Final owner pivot mesh contract. CERN-OHL-S-2.0."""
def validate_visible_mechanism(bundle):
    names={p['name'] for p in bundle['parts']}
    required={'PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR'}|{f'PF_CommercialStrap{i}' for i in range(1,5)}
    assert required <= names
    assert sum(n.startswith('PF_CommercialStrap') for n in names)==4
    assert sum(n.startswith('PF_StrapScrew') for n in names)==8
    assert sum(n.startswith('PF_SupportMountScrew') for n in names)==6
    assert all(not any(k in n.lower() for k in ('prop','bush','journal','bearing','clevis','keeper','pivotaxis','positivepin','stowpin')) for n in names if n.startswith('PF_'))
    assert set(bundle['states'])=={'PLAY','SERVICE','LIFT-OUT','EXPLODED'}
    for state in ('SERVICE','LIFT-OUT'):
        assert bundle['states'][state]['PF_BasePlywood']
        assert bundle['states'][state]['PLAYFIELD_ENVELOPE']
    assert not bundle['review']['manufacturing_ready']
