import ast
import pytest
import jsonschema
import time as ttime
from datetime import datetime
from bluesky.plans import scan, grid_scan
import bluesky.preprocessors as bpp
import bluesky.plan_stubs as bps
from bluesky.preprocessors import SupplementalData
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.utils import new_uid
from event_model import RunRouter


def test_hints(RE, hw):
    motor = hw.motor
    expected_hint = {'fields': [motor.name]}
    assert motor.hints == expected_hint
    collector = []

    def collect(*args):
        collector.append(args)

    RE(scan([], motor, 1, 2, 2), {'descriptor': collect})
    name, doc = collector.pop()
    assert doc['hints'][motor.name] == expected_hint


def test_simple(RE, hw):
    bec = BestEffortCallback()
    RE.subscribe(bec)
    RE(scan([hw.ab_det], hw.motor, 1, 5, 5))


def test_disable(RE, hw):
    det, motor = hw.ab_det, hw.motor
    bec = BestEffortCallback()
    RE.subscribe(bec)

    bec.disable_table()

    RE(scan([det], motor, 1, 5, 5))
    assert bec._table is None

    bec.enable_table()

    RE(scan([det], motor, 1, 5, 5))
    assert bec._table is not None

    bec.peaks.com
    bec.peaks['com']
    assert ast.literal_eval(repr(bec.peaks)) == vars(bec.peaks)

    bec.clear()
    assert bec._table is None

    # smoke test
    bec.disable_plots()
    bec.enable_plots()
    bec.disable_baseline()
    bec.enable_baseline()
    bec.disable_heading()
    bec.enable_heading()


def test_blank_hints(RE, hw):
    bec = BestEffortCallback()
    RE.subscribe(bec)
    RE(scan([hw.ab_det], hw.motor, 1, 5, 5, md={'hints': {}}))


def test_with_baseline(RE, hw):
    bec = BestEffortCallback()
    RE.subscribe(bec)
    sd = SupplementalData(baseline=[hw.det])
    RE.preprocessors.append(sd)
    RE(scan([hw.ab_det], hw.motor, 1, 5, 5))


def test_underhinted_plan(RE, hw):
    bec = BestEffortCallback()
    RE.subscribe(bec)

    @bpp.run_decorator()
    def broken_plan(dets):
        yield from bps.trigger_and_read(dets)

    RE(broken_plan([hw.det]))


def test_live_grid(RE, hw):
    bec = BestEffortCallback()
    RE.subscribe(bec)
    RE(grid_scan([hw.det4], hw.motor1, 0, 1, 1, hw.motor2, 0, 1, 2, True))


def test_push_start_document(capsys):
    """ Pass the start document to BEC and verify if the scan information is printed correctly"""

    bec = BestEffortCallback()

    uid = new_uid()
    time = ttime.time()
    scan_id = 113435  # Just some arbitrary number

    # Include minimum information needed to print the header
    bec("start", {"scan_id": scan_id, "time": time, "uid": uid})

    captured = capsys.readouterr()
    assert f"Transient Scan ID: {scan_id}" in captured.out, \
        "BestEffortCallback: Scan ID is not printed correctly"

    tt = datetime.fromtimestamp(time).utctimetuple()
    assert f"Time: {ttime.strftime('%Y-%m-%d %H:%M:%S', tt)}" in captured.out, \
        "BestEffortCallback: Scan time is not printed correctly"
    assert f"Persistent Unique Scan ID: '{uid}'" in captured.out, \
        "BestEffortCallback: Scan UID is not printed correctly"


def test_multirun_nested_plan(capsys, caplog, RE, hw):
    # This test only checks if the plan runs without crashing. If BEC crashes,
    #   the plan will still run, but data will not be displayed.
    @bpp.set_run_key_decorator(run="inner_run")
    def plan_inner():
        yield from grid_scan([hw.det4], hw.motor1, 0, 1, 1, hw.motor2, 0, 1, 2, True)

    def sequence():
        for n in range(5):
            yield from bps.mov(hw.motor, n * 0.1 + 1)
            yield from bps.trigger_and_read([hw.det1])

    @bpp.set_run_key_decorator(run="outer_run")
    @bpp.stage_decorator([hw.det1, hw.motor])
    @bpp.run_decorator(md={})
    def plan_outer():
        yield from sequence()
        # Call inner plan from within the plan
        yield from plan_inner()
        # Run another set of commands
        yield from sequence()

    # The first test should fail. We check if expected error message is printed in case
    #   of failure.
    bec = BestEffortCallback()
    bec_token = RE.subscribe(bec)
    RE(plan_outer())

    captured = capsys.readouterr()

    # Check for the number of runs (the number of times UID is printed in the output)
    scan_uid_substr = "Persistent Unique Scan ID"
    n_runs = captured.out.count(scan_uid_substr)
    assert n_runs == 2, "scan output contains incorrect number of runs"
    # Check if the expected error message is printed once the callback fails. The same
    #   substring will be used in the second part of the test to check if BEC did not fail.
    err_msg_substr = "is being suppressed to not interrupt plan execution"
    assert err_msg_substr in str(caplog.text), \
        "Best Effort Callback failed, but expected error message was not printed"

    RE.unsubscribe(bec_token)
    caplog.clear()

    # The second test should succeed, i.e. the error message should not be printed
    def factory(name, doc):
        bec = BestEffortCallback()
        return [bec], []
    rr = RunRouter([factory])
    RE.subscribe(rr)
    RE(plan_outer())

    captured = capsys.readouterr()
    n_runs = captured.out.count(scan_uid_substr)
    assert n_runs == 2, "scan output contains incorrect number of runs"
    assert err_msg_substr not in caplog.text, \
        "Best Effort Callback failed while executing nested plans"


@pytest.mark.xfail(not (jsonschema.__version__.split('.') < ['3', ]),
                   reason='Deprecations in jsonschema')
def test_plot_ints(RE):
    from ophyd import Signal
    from bluesky.callbacks.best_effort import BestEffortCallback
    from bluesky.plans import count
    import bluesky.plan_stubs as bps

    bec = BestEffortCallback()
    RE.subscribe(bec)

    s = Signal(name='s')
    RE(bps.mov(s, int(0)))
    assert s.describe()['s']['dtype'] == 'integer'
    s.kind = 'hinted'
    with pytest.warns(None) as record:
        RE(count([s], num=35))

    assert len(record) == 0


def test_plot_prune_fifo(RE, hw):
    bec = BestEffortCallback()
    RE.subscribe(bec)

    num_pruned = 2

    # create the LivePlot
    RE(bps.repeater(num_pruned, scan, [hw.ab_det], hw.motor, 1, 5, 5))

    # test it
    assert len(bec._live_plots) == 1

    # get the reference key for our LivePlot dict
    uuid = next(iter(bec._live_plots))
    assert len(bec._live_plots[uuid]) == 1

    # get reference key for our detector
    det_name = next(iter(bec._live_plots[uuid]))
    # should be same as hw.ab_det.a.name (`.a` comes from .read_attrs[0]), prove it now
    assert det_name == hw.ab_det.a.name

    # get the LivePlot object
    lp = bec._live_plots[uuid][det_name]

    assert lp is not None
    assert len(lp.ax.lines) == num_pruned

    # prune the LivePlot (has no effect since we have exact number to keep)
    bec.plot_prune_fifo(num_pruned, hw.motor, hw.ab_det.a)
    assert len(lp.ax.lines) == num_pruned

    # add more lines to the LivePlot
    RE(bps.repeater(num_pruned, scan, [hw.ab_det], hw.motor, 1, 5, 5))

    # get the LivePlot object, again, in case the UUID was changed
    assert len(bec._live_plots) == 1
    uuid = next(iter(bec._live_plots))
    lp = bec._live_plots[uuid][det_name]
    assert lp is not None
    assert len(lp.ax.lines) == num_pruned * 2

    # prune again, this time reduces number of lines
    bec.plot_prune_fifo(num_pruned, hw.motor, hw.ab_det.a)
    assert len(lp.ax.lines) == num_pruned
