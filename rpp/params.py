from spec import rust_spec
from render import RenderParams

from collections import OrderedDict
import random
import copy
import csv


abbr = {
    'koscR': 'r  ',
    'koscFreq': 'frq',
    'koscError': 'err',
    'lowPassPot': 'lp',
    'preAmpPot': 'pre',
    'powAmpPot': 'pow',
    'lfoPot': 'lfo',
    'lfoCSwitch': 'cap',
    'lfoWidth': 'wdth',
    'lfoIPhase': 'phz',
    'lfoLowPassPot': 'lp2',
    'vactrolAttack': 'atk',
    'vactrolDecay': 'dcy',
    'vactrolHysteresis': 'hyst',
    'vactrolDepth': 'dpth',
    'vactrolScalar': 'vsc',
    'lfoGate': 'lfx',
    'vactrolGate': 'vctx',
    'fbackX': 'fbX',
    'fbackY': 'fbY',
    'fbackZ': 'fbZ',
    'outX': 'oX',
    'outY': 'oY',
    'outZ': 'oZ',
}

def to_snake_case(k):
    x = {
        'koscR': 'kosc_r',
        'koscFreq': 'kosc_freq',
        'koscError': 'kosc_error',
        'lowPassPot': 'lowpass_pot',
        'preAmpPot': 'preamp_pot',
        'powAmpPot': 'powamp_pot',
        'lfoPot': 'lfo_pot',
        'lfoCSwitch': 'lfo_cswitch',
        'lfoWidth': 'lfo_width',
        'lfoIPhase': 'lfo_iphase',
        'lfoLowPassPot': 'lfo_lowpass_pot',
        'vactrolAttack': 'vactrol_attack',
        'vactrolDecay': 'vactrol_decay',
        'vactrolHysteresis': 'vactrol_hysteresis',
        'vactrolDepth': 'vactrol_depth',
        'vactrolScalar': 'vactrol_scalar',
        'lfoGate': 'lfo_gate',
        'vactrolGate': 'vactrol_gate',
        'fbackScalars': 'fback_scalars',
        'outScalars': 'out_scalars',
    }
    return x[k] if k in x else k

def to_camel_case(k):
    x = {
        'kosc_r': 'koscR',
        'kosc_freq': 'koscFreq',
        'kosc_error': 'koscError',
        'lowpass_pot': 'lowPassPot',
        'preamp_pot': 'preAmpPot',
        'powamp_pot': 'powAmpPot',
        'lfo_pot': 'lfoPot',
        'lfo_cswitch': 'lfoCSwitch',
        'lfo_width': 'lfoWidth',
        'lfo_iphase': 'lfoIPhase',
        'lfo_lowpass_pot': 'lfoLowPassPot',
        'vactrol_attack': 'vactrolAttack',
        'vactrol_decay': 'vactrolDecay',
        'vactrol_hysteresis': 'vactrolHysteresis',
        'vactrol_depth': 'vactrolDepth',
        'vactrol_scalar': 'vactrolScalar',
        'lfo_gate': 'lfoGate',
        'vactrol_gate': 'vactrolGate',
        'fback_scalars': 'fbackScalars',
        'out_scalars': 'outScalars',
    }
    return x[k] if k in x else k

class FeedbackParams:
    size = 24

    def __init__(self, params_dict):
        self.params = params_dict

    @classmethod
    def from_dict(cls, params_dict):
        """Create a FeedbackParams from dict. Guards against out-of-order params list."""
        fbp = cls.default_params()
        for k,v in params_dict.items():
            fbp.params[k] = v
        return fbp

    @classmethod
    def default_params(cls, spec=None):
        pdict = OrderedDict([
            ('koscR', 18.6),
            ('koscFreq', 0.85),
            ('koscError', 4.0),
            ('lowPassPot', 1.0 - 0.15),
            ('preAmpPot', 0.75 - 0.55),
            ('powAmpPot', 0.9),
            ('lfoPot', 0.33),
            ('lfoCSwitch', 0),
            ('lfoWidth', 0.5),
            ('lfoIPhase', 0.0),
            ('lfoLowPassPot', 0.5),
            ('vactrolAttack', 0.027),
            ('vactrolDecay', 4.0),
            ('vactrolHysteresis', 6.0),
            ('vactrolDepth', 2.0),
            ('vactrolScalar', 1.0),
            ('lfoGate', 1.0),
            ('vactrolGate', 1.0),
            ('fbackX', 1.0),
            ('fbackY', 1.0),
            ('fbackZ', 1.0),
            ('outX', 1.0),
            ('outY', 1.0),
            ('outZ', 1.0),
        ])
        
        if spec is not None:
            for k in spec.keys():
                pdict[k] = spec[k].default if spec[k].default is not None else pdict[k]

        return cls(pdict)

    @classmethod
    def from_list(cls, plist):
        return cls(
            OrderedDict([
                ('koscR', plist[0]),
                ('koscFreq', plist[1]),
                ('koscError', plist[2]),
                ('lowPassPot', plist[3]),
                ('preAmpPot', plist[4]),
                ('powAmpPot', plist[5]),
                ('lfoPot', plist[6]),
                ('lfoCSwitch', plist[7]),
                ('lfoWidth', plist[8]),
                ('lfoIPhase', plist[9]),
                ('lfoLowPassPot', plist[10]),
                ('vactrolAttack', plist[11]),
                ('vactrolDecay', plist[12]),
                ('vactrolHysteresis', plist[13]),
                ('vactrolDepth', plist[14]),
                ('vactrolScalar', plist[15]),
                ('lfoGate', plist[16]),
                ('vactrolGate', plist[17]),
                ('fbackX', plist[18]),
                ('fbackY', plist[19]),
                ('fbackZ', plist[20]),
                ('outX', plist[21]),
                ('outY', plist[22]),
                ('outZ', plist[23]),
            ])
        )

    def map_spec(self, spec):
        """Map thru the spec. Returns a new copy."""
        return FeedbackParams(OrderedDict([(k, spec.map_spec(k, v)) for k,v in self.params.items()]))

    def randomize(self, randorams, spec=rust_spec()):
        """Randomize randorams. Returns a new copy."""
        beta = copy.deepcopy(self)
        for k in randorams:
            beta.params[k] = spec.map_spec(k, random.random())
        return beta

    def serialize(self):
        """Convert to list. For sending data over the network."""
        return [v for v in self.params.values()]

    def to_vec(self, params=None, unmap=False, spec=None):
        """Convert to vector. For data analysis."""
        params = self.params.keys() if params is None else params 
        map_func = (lambda k,v: spec.unmap_spec(k, v)) if unmap is True else (lambda k,v: v)
        return [map_func(k, v) for k,v in self.params.items() if k in params]

    def to_dataframe(self, params=None, unmap=False, spec=None, suffix=''):
        """Convert to dataframe. For data analysis."""
        params = self.params.keys() if params is None else params
        map_func = (lambda k,v: spec.unamp_spec(k, v)) if unmap is True else (lambda k,v: v)
        return OrderedDict([('{0}{1}'.format(k, suffix), map_func(k, v)) 
                            for k,v in self.params.items() if k in params])

    def to_json(self):
        """Return a json serializable format."""
        rs_dict = OrderedDict([(to_snake_case(k), v) for k,v in self.params.items()])
        del rs_dict['fbackX']
        del rs_dict['fbackY']
        del rs_dict['fbackZ']
        del rs_dict['outX']
        del rs_dict['outY']
        del rs_dict['outZ']
        rs_dict.update({'fback_scalars': [self.params['fbackX'], self.params['fbackY'], self.params['fbackZ']]})
        rs_dict.update({'out_scalars': [self.params['outX'], self.params['outY'], self.params['outZ']]})
        return rs_dict

    @classmethod
    def from_json(cls, dct):
        """Retun a FeedbackParams from JSON file dictionary."""
        py_dict = OrderedDict([(to_camel_case(k), v) for k,v in dct.items()])
        del py_dict['fbackScalars']
        del py_dict['outScalars']
        py_dict.update({'fbackX': dct['fback_scalars'][0]})
        py_dict.update({'fbackY': dct['fback_scalars'][1]})
        py_dict.update({'fbackZ': dct['fback_scalars'][2]})
        py_dict.update({'outX': dct['out_scalars'][0]})
        py_dict.update({'outY': dct['out_scalars'][1]})
        py_dict.update({'outZ': dct['out_scalars'][2]})
        return FeedbackParams.from_dict(py_dict)

    def keys(self):
        return self.params.keys()

    def values(self):
        return self.params.values()

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, val):
        if key not in self.params:
            raise LookupError('Key \'{}\' not found in params dict'.format(key))
        else:
            self.params[key] = val

    def __repr__(self):
        return '<Params({0.params!r}>'.format(self)

class FeedbackQuadParams:
    size = FeedbackParams.size * 4

    def __init__(self, params_dicts):
        self.params = params_dicts

    @classmethod
    def default_params(cls, spec=None):
        return cls([FeedbackParams.default_params(spec=spec) for i in range(4)])

    def randomize(self, randorams, spec=rust_spec()):
        """randomize randorams. Returns a new copy."""
        beta = copy.deepcopy(self)
        for i in range(len(beta.params)):
            beta.params[i] = beta.params[i].randomize(randorams, spec=spec)
        return beta

    def serialize(self):
        """Convert to list."""
        return reduce(lambda x,y: x+y, [p.serialize() for p in self.params])

    def pretty_csv(self, filename='test.csv'):
        """Print as CSV. This is for display purposes NOT save and recall."""
        with open(filename, 'wb') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow([abbr[k] for k in FeedbackParams.default_params().keys()])
            for p in self.params:
                wr.writerow(['{}'.format((round(v,2))) for v in p.values()])

    def to_csv(self, filename='test.csv'):
        """Print as CSV. This is for save and recall."""
        with open(filename, 'wb') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(FeedbackParams.default_params().keys())
            for p in self.params:
                wr.writerow(p.values())

    def to_vec(self, params=None, unmap=False, spec=None):
        """Convert to vector. For data analysis."""
        return sum([p.to_vec(params=params, unmap=unmap, spec=spec) for p in self.params], [])

    def to_dataframe(self, params=None, unmap=False, spec=None):
        """Convert to dataframe. For data analysis."""
        def merge(x):
            """Merges a list of OrderedDicts."""
            def helper(x,y): x.update(y); return x
            return reduce(helper, [OrderedDict()] + x)
        return merge([p.to_dataframe(params=params, unmap=unmap, spec=spec, suffix=['A', 'B', 'C', 'D'][i]) 
                      for i,p in enumerate(self.params)])

    def to_json(self):
        """Return a json serializable format."""
        return [p.to_json() for p in self.params]

    @classmethod
    def from_json(cls, list_of_JSON_dicts):
        """Return a FeedbackQuadParams from JSON file dictionary."""
        return FeedbackQuadParams([FeedbackParams.from_json(dct) for dct in  list_of_JSON_dicts])

    def deepcopy(self):
        """Return a deep copy. Really just a convenience for copy.deepcopy()."""
        return copy.deepcopy(self)

    def setall(self, param, val):
        """Set param for all four FeedbackParams. Returns self."""
        for pdict in self.params:
            pdict[param] = val
        return self

    def __getitem__(self, index):
        return self.params[index]

    def __setitem__(self, index, val):
        self.params[index] = val

    def __repr__(self):
        return '<FeedbackQuadParams({0.params!r}>'.format(self)

class Sample:
    """Keep track of render params and synth param.s"""

    def __init__(self, topology, render_params, synth_params):
        self.topology = topology
        self.render_params = render_params
        self.synth_params = synth_params

    def to_json(self):
        return OrderedDict([
            ("topology", self.topology),
            ("render_params", self.render_params),
            ("synth_params", self.synth_params.to_json())
        ])

    @classmethod
    def from_json(cls, dct):
        """Return a Sample from JSON file dictionary."""
        return Sample(
            topology = dct['topology'],
            render_params = RenderParams.from_json(dct['render_params']),
            synth_params = FeedbackQuadParams.from_json(dct['synth_params']) # hardcoded for now
        )

    def __repr__(self):
        return '<Sample(topology: {0.topology!r}, render_params: {0.render_params!r}, synth_params: {0.synth_params!r})>'.format(self)


def test_feedbackparams_json():
    """Test to/from json for FeedbackParams."""
    import json
    alpha = FeedbackParams.default_params()
    with open("data_file.json", "w") as write_file:
        json.dump(alpha.to_json(), write_file)
    with open("data_file.json", "r") as read_file:
        beta = FeedbackParams.from_json(json.loads(read_file.readline()))
    print(alpha)
    print(beta)
    print(alpha.params == beta.params)

def test_json():
    import json
    alpha = Sample("FeedbackQuad", render.RenderParams(), FeedbackQuadParams.default_params())
    beta = Sample("FeedbackQuad", render.RenderParams(), FeedbackQuadParams.default_params())
    with open("data_file.json", "w") as write_file:
        json.dump(alpha.to_json(), write_file)
        write_file.write('\n\n')
        json.dump(beta.to_json(), write_file)

def test_to_vec():
    import spec
    alpha = FeedbackParams.default_params(spec=spec.rust_spec())
    print alpha.to_vec(params=['koscR'], unmap=True, spec=spec.rust_spec())


if __name__ == "__main__":
    test_json()
    test_to_vec()
