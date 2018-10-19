import math
from collections import namedtuple


SpecElem = namedtuple('SpecElem', ['lo', 'hi', 'curve', 'default'])

class ControlSpec: 
    """A very basic SC-style control spec."""

    def __init__(self):
        self.data = dict()

    def add(self, param, spec, default=None):
        """Store in dict."""
        self.data[param] = SpecElem(spec[0], spec[1], spec[2], default)
        # self.data[param] = spec

    def map_spec(self, param, val):
        """Map from normal."""
        lo, hi, curve, default = self.data[param]
        val = self.clip(val, 0.0, 1.0)
        if curve is 'linear':
            return self.linear_map(float(val), float(lo), float(hi))
        if curve is 'exp':
            return self.exp_map(float(val), float(lo), float(hi))
        if curve is 'binary': 
            return self.binary_map(val)

    def unmap_spec(self, param, val):
        """Unmap to normal."""
        lo, hi, curve, default = self.data[param]
        clip_lo = min(lo, hi)
        clip_hi = max(lo, hi)
        val = self.clip(val, clip_lo, clip_hi)
        if curve is 'linear':
            return self.linear_unmap(float(val), float(lo), float(hi))
        if curve is 'exp':
            return self.exp_unmap(float(val), float(lo), float(hi))
        if curve is 'binary':
            return self.binary_unmap(val)

    def linear_map(self, val, lo, hi):
        """Linear mapping."""
        return val * (hi - lo) + lo

    def linear_unmap(self, val, lo, hi):
        """Linear unmapping."""
        return (val - lo) / (hi - lo)

    def exp_map(self, val, lo, hi):
        """Exponential mapping."""
        return pow(hi / lo, val) * lo

    def exp_unmap(self, val, lo, hi):
        """Exponential unmapping."""
        return math.log(val / lo) / math.log(hi / lo)

    def binary_map(self, val):
        """Binary mapping."""
        return 0 if val <= 0.5 else 1

    def binary_unmap(self, val):
        """Binary unmaping."""
        return float(val)

    def clip(self, val, lo, hi):
        """Clip to hi and lo."""
        return lo if val < lo else hi if val > hi else val

    def keys(self):
        return self.data.keys()

    def __getitem__(self, key):
        return self.data[key]

def default_spec():
    spec = ControlSpec()
    spec.add('koscFreq', [1, 1, 'linear'])
    spec.add('koscError', [0.5, 15, 'linear'])
    spec.add('lowPassPot', [0, 1, 'linear'])
    # --- OSC1 --- 
    spec.add('koscRA', [0.1, 40.0, 'exp'])
    spec.add('preAmpPotA', [0, 1, 'linear'])
    spec.add('powAmpPotA', [0, 1, 'linear'])
    spec.add('lfoPotA', [0.1, 1, 'linear'])
    spec.add('lfoCapSwitchA', [0, 1, 'linear', 1])
    spec.add('lfoIPhaseA', [0, 1, 'linear'])
    spec.add('lfoLowPassPotA', [0, 1, 'linear'])
    spec.add('vactrolScalarA', [0.1, 2.0, 'linear'])
    spec.add('vactrolAttackA', [0.001, 0.3, 'exp'])
    spec.add('vactrolDecayA', [0.01, 3.0, 'exp'])
    spec.add('vactrolHysteresisA', [0.0, 100.0, 'linear'])
    spec.add('vactrolDepthA', [1.0, 6.0, 'linear'])
    spec.add('koscGateA', [0, 1, 'linear', 1])
    spec.add('vactrolGateA', [0, 1, 'linear', 1])
    spec.add('lfoGateA', [0, 1, 'linear', 1])
    spec.add('fbackXA', [0, 1, 'linear'])
    spec.add('fbackYA', [0, 1, 'linear'])
    spec.add('fbackZA', [0, 1, 'linear'])
    spec.add('outXA', [0, 1, 'linear'])
    spec.add('outYA', [0, 1, 'linear'])
    spec.add('outZA', [0, 1, 'linear'])
    # --- OSC2 --- 2 
    spec.add('koscRB', [0, 40.0, 'linear'])
    spec.add('preAmpPotB', [0, 1, 'linear'])
    spec.add('powAmpPotB', [0, 1, 'linear'])
    spec.add('lfoPotB', [0.1, 1, 'linear'])
    spec.add('lfoCapSwitchB', [0, 1, 'binary'])
    spec.add('lfoLowPassPotB', [0, 1, 'linear'])
    spec.add('vactrolScalarB', [0.1, 2.0, 'linear'])
    spec.add('vactrolAttackB', [0.001, 0.03, 'exp'])
    spec.add('vactrolDecayB', [0.01, 3.0, 'exp'])
    spec.add('vactrolHysteresisB', [0.0, 100.0, 'linear'])
    spec.add('vactrolDepthB', [1.0, 6.0, 'linear'])
    spec.add('koscGateB', [0, 1, 'linear', 1])
    spec.add('vactrolGateB', [0, 1, 'linear', 1])
    spec.add('lfoGateB', [0, 1, 'linear', 1])
    spec.add('fbackXB', [0, 1, 'linear'])
    spec.add('fbackYB', [0, 1, 'linear'])
    spec.add('fbackZB', [0, 1, 'linear'])
    spec.add('outXB', [0, 1, 'linear'])
    spec.add('outYB', [0, 1, 'linear'])
    spec.add('outZB', [0, 1, 'linear'])
    return spec

def rust_spec():
    spec = ControlSpec()
    spec.add('koscFreq', [0, 1, 'linear'])
    spec.add('koscError', [0.5, 15, 'linear'])
    spec.add('koscR', [0.1, 40.0, 'exp'])
    spec.add('lowPassPot', [0, 1, 'linear'])
    spec.add('preAmpPot', [0, 1, 'linear'])
    spec.add('powAmpPot', [0, 1, 'linear'])
    spec.add('lfoPot', [0.1, 1, 'linear'])
    spec.add('lfoCSwitch', [0, 1, 'binary'])
    spec.add('lfoWidth', [0.1, 1, 'linear'])
    spec.add('lfoIPhase', [0, 1, 'linear'])
    spec.add('lfoLowPassPot', [0, 1, 'linear'])
    spec.add('vactrolAttack', [0.001, 0.3, 'exp'])
    spec.add('vactrolDecay', [0.01, 3.0, 'exp'])
    spec.add('vactrolHysteresis', [0.0, 100.0, 'linear'])
    spec.add('vactrolDepth', [1.0, 6.0, 'linear'])
    spec.add('vactrolScalar', [0.1, 2.0, 'linear'])
    spec.add('vactrolGate', [0, 1, 'linear'])
    spec.add('lfoGate', [0, 1, 'linear'])
    spec.add('fbackX', [0, 1, 'linear'])
    spec.add('fbackY', [0, 1, 'linear'])
    spec.add('fbackZ', [0, 1, 'linear'])
    spec.add('outX', [0, 1, 'linear'])
    spec.add('outY', [0, 1, 'linear'])
    spec.add('outZ', [0, 1, 'linear'])
    return spec

def test_linear():
    spec = ControlSpec()
    spec.add('koscFreq', [1, 99, 'linear'])
    print(spec.map_spec('koscFreq', -0.1) == 1.0)
    print(spec.map_spec('koscFreq', 0.0) == 1.0)
    print(spec.map_spec('koscFreq', 0.5) == 50.0)
    print(spec.map_spec('koscFreq', 1.0) == 99.0)
    print(spec.map_spec('koscFreq', 1.1) == 99.0)
    print(spec.unmap_spec('koscFreq', 0) == 0.0)
    print(spec.unmap_spec('koscFreq', 1) == 0.0)
    print(spec.unmap_spec('koscFreq', 50) == 0.5)
    print(spec.unmap_spec('koscFreq', 99) == 1.0)
    print(spec.unmap_spec('koscFreq', 100) == 1.0)

def test_exp():
    spec = ControlSpec()
    spec.add('koscFreq', [0.001, 100, 'exp'])
    print(spec.map_spec('koscFreq', -0.1) == 0.001)
    print(spec.map_spec('koscFreq', 0.0) == 0.001)
    print(abs(spec.map_spec('koscFreq', 0.5) - 0.316227766017) < 1e-12)
    print(spec.map_spec('koscFreq', 1) == 100.0)
    print(spec.map_spec('koscFreq', 1.1) == 100.0)
    print(spec.unmap_spec('koscFreq', 0.0) == 0.0)
    print(spec.unmap_spec('koscFreq', 0.001) == 0.0)
    print(abs(spec.unmap_spec('koscFreq', 50) - 0.939794000867) <1e-12)
    print(spec.unmap_spec('koscFreq', 100) == 1.0)
    print(spec.unmap_spec('koscFreq', 101) == 1.0)

def test_binary():
    spec = ControlSpec()
    spec.add('lfoCSwitch', [0, 1, 'binary'])
    print(spec.map_spec('lfoCSwitch', -0.1) == 0.0)
    print(spec.map_spec('lfoCSwitch', 0.0) == 0.0)
    print(spec.map_spec('lfoCSwitch', 0.25) == 0.0)
    print(spec.map_spec('lfoCSwitch', 0.5) == 0.0)
    print(spec.map_spec('lfoCSwitch', 0.75) == 1.0)
    print(spec.map_spec('lfoCSwitch', 1.0) == 1.0)
    print(spec.map_spec('lfoCSwitch', 1.1) == 1.0)
    print(spec.unmap_spec('lfoCSwitch', 0) == 0.0)
    print(spec.unmap_spec('lfoCSwitch', 1) == 1.0)

if __name__ == "__main__":
    test_linear()
    test_exp()
    test_binary()
