import oscmsg
import display

from collections import OrderedDict
import OSC
import math
import datetime
import time
from threading import Thread


class RenderParams(OrderedDict):
    """Keeps track of render params."""

    def __init__(self, render_id="00", folder='~', filename='sample.wav', duration=20.0, wait=0.0):
        OrderedDict.__init__(self, [
            ('render_id', render_id),
            ('folder', folder),
            ('filename', filename),
            ('duration', duration),
            ('wait', wait)
        ])

    @classmethod
    def from_json(cls, dct):
        """Return a RenderParams from JSON file dictionary."""
        return RenderParams(**dct)

# class Sample:
#     """Keeps track of render params."""

#     def __init__(self, params=None, folder='~', filename='sample.wav', duration=20.0, wait=0.0):
#         self.rid = None
#         self.folder = folder
#         self.filename = filename
#         self.duration = duration
#         self.wait = wait
#         self.params = params if params is not None else FeedbackParams()

#     def __repr__(self):
#         return '<Sample({0.filename!r})>'.format(self)

class Renderer:
    """Does the rendering."""

    def __init__(self, osc_client, py_server):
        self.osc_client = osc_client
        self.py_server = py_server

    def _new_rid(self):
        """Generate unique render id."""
        a = datetime.datetime.now()
        rid = '{0}{1}{2}{3}{4}{5}{6}'.format(a.year, a.month, a.day, a.hour, a.minute, a.second, a.microsecond)
        return rid

    def render(self, sample, verbose=True):
        """Render a single sample."""
        rid = self._new_rid()
        sample.render_params['render_id'] = rid

        # new client
        self.osc_client.send(oscmsg.new())
        time.sleep(0.1)

        # set folder
        self.osc_client.send(oscmsg.set_folder(sample.render_params['folder']))
        # set filename
        self.osc_client.send(oscmsg.set_filename(sample.render_params['filename'] + '.wav'))
        # set duration
        self.osc_client.send(oscmsg.set_duration(sample.render_params['duration']))
        # set wait
        self.osc_client.send(oscmsg.set_wait(sample.render_params['wait']))
        # set id
        self.osc_client.send(oscmsg.set_render_id(sample.render_params['render_id']))
        # new topology
        self.osc_client.send(oscmsg.new_with_default_params())
        time.sleep(0.1)

        # set params
        for i in range(4):
            self.osc_client.send(oscmsg.set_params(sample.synth_params[i].serialize(), index=i))
        time.sleep(0.1)

        # new topology with current params
        self.osc_client.send(oscmsg.new_with_current_params())
        time.sleep(0.1)

        # render 
        self.osc_client.send(oscmsg.render_static())
        print('{0}requesting to render: {1}'.format(display.TO_RS, rid))
        time.sleep(0.1)

        # write params to file
        sample.synth_params.pretty_csv('{0}/{1}.csv'.format(sample.render_params['folder'], sample.render_params['filename']))

        # write params to file
        sample.synth_params.to_csv('{0}/{1}_data.csv'.format(sample.render_params['folder'], sample.render_params['filename']))

        return self

    def render_and_do(self, sample, do_func, func_args, verbose=True):
        """Render sample and do do_func upon completion."""
        self.render(sample, verbose=verbose)
        # function to call upon complete
        def foo(pat, tags, args, source):
            # print('{0}render complete: {1}'.format(display.FRM_RS, sample.rid))
            self.py_server.server.delMsgHandler('/{0}'.format(sample.render_params['render_id']))
            # launch analysis on separate thread
            t = Thread(target=do_func, args=func_args)
            t.start()
        # add to message handler
        self.py_server.server.addMsgHandler('/{0}'.format(sample.render_params['render_id']), foo)
        return self

    def batch_render(self, samples, batch_size=8, deleteme=False):
        """Render samples in groups of batch_size at a time."""
        for bi in range(int(math.floor((len(samples) - 1) / batch_size)) + 1):
            batch = samples[bi * batch_size: min((bi + 1) * batch_size, len(samples))]
            # helper func to keep track of who is not yet done
            notifications = [True]*len(batch)
            def notify_func(index=0):
                notifications[index] = False
            # render all in batch 
            for i,sample in enumerate(batch):
                self.render_and_do(sample, notify_func, (i,))
            print('{0}waiting for batch {1}\n'. format(display.WAITING, bi)),
            while any(notifications): pass
        return self

    def render_and_score(self, sample, filename='sample', verbose=True, deleteme=True):
        """Render and score fitness."""
        self.render_and_do(sample, sample.fitness, (self, deleteme), filename, verbose)
        return self

    def batch_render_and_score(self, samples, batch_size=8, deleteme=True):
        """Render samples in groups of batch_size at a time."""
        for bi in range(int(math.floor((len(samples) - 1) / batch_size)) + 1):
            batch = samples[bi * batch_size: min((bi + 1) * batch_size, len(samples))]
            # print('rendering batch {0}'.format(bi))
            for sample in batch:
                self.render_and_score(sample, deleteme=deleteme)
            print('{0}waiting for batch {1}\n'. format(display.WAITING, bi)),
            while any([sample.score is None for sample in batch]): pass
        return self

    def batch_render_and_score_single_analysis_thread(self, samples, batch_size=8, deleteme=True):
        """Render samples in groups of batch_size at a time."""
        for bi in range(int(math.floor((len(samples) - 1) / batch_size)) + 1):
            batch = samples[bi * batch_size: min((bi + 1) * batch_size, len(samples))]
            # print('rendering batch {0}'.format(bi))
            notifications = [True]*len(batch)
            def notify_func(index=0):
                notifications[index] = False
            for i,sample in enumerate(batch):
                self.render_and_do(sample, notify_func, (i,))
            print('{0}waiting for batch {1}\n'. format(display.WAITING, bi)),
            while any(notifications): 
                pass
            map(lambda sample: sample.fitness(self), batch)
        return self

    def __repr__(self):
        return '<Renderer()>'.format(self)
