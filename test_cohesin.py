### CLAUDE GENERATED TEST FILE


import random

import pytest

from dataclass import Sequence, OrderedPair, Cohesin


def make(ctcf, start_left, start_right=None, length=100):
    """Build a Sequence with the given CTCF sites and a bound Cohesin
    placed by hand (bypasses the random bind())."""
    if start_right is None:
        start_right = start_left
    seq = Sequence(length=length, ctcf_positions=set(ctcf))
    c = Cohesin(position=OrderedPair(start_left, start_right), bound=True)
    seq.cohesin_positions.update({start_left, start_right})
    return seq, c


def run(c, seq, steps, prob_block=1.0):
    for _ in range(steps):
        c.step(seq, prob_block)


# ---------- blocking at CTCF sites (deterministic, prob_block=1.0) ----------

def test_right_end_stops_before_ctcf():
    seq, c = make({10}, start_left=8)
    run(c, seq, 20)
    assert c.position.right == 9


def test_left_end_stops_after_ctcf():
    seq, c = make({40}, start_left=50)
    run(c, seq, 50)
    assert c.position.left == 41


def test_loop_stalls_between_two_sites():
    seq, c = make({40, 60}, start_left=50)
    run(c, seq, 100)
    assert (c.position.left, c.position.right) == (41, 59)
    assert c.loop_size() == 18


def test_stalled_loop_size_stays_constant():
    seq, c = make({40, 60}, start_left=50)
    run(c, seq, 30)
    size_after_stall = c.loop_size()
    run(c, seq, 50)
    assert c.loop_size() == size_after_stall


def test_ends_are_blocked_independently():
    # Only the right side has a CTCF site; the left end keeps extruding.
    seq, c = make({55}, start_left=50)
    run(c, seq, 20)
    assert c.position.right == 54
    assert c.position.left == 30


# ---------- no blocking when prob_block=0 ----------

def test_no_blocking_when_prob_zero():
    seq, c = make({40, 60}, start_left=50)
    run(c, seq, 15, prob_block=0.0)
    assert c.position.left == 35
    assert c.position.right == 65


# ---------- no CTCF sites ----------

def test_moves_one_position_per_step_without_ctcf():
    seq, c = make(set(), start_left=50)
    c.step(seq)
    assert (c.position.left, c.position.right) == (49, 51)


# ---------- sequence boundaries ----------

def test_stops_at_sequence_edges():
    seq, c = make(set(), start_left=5, start_right=95, length=100)
    run(c, seq, 50)
    assert c.position.left == 0
    assert c.position.right == 99


# ---------- cohesin_positions bookkeeping ----------

def test_cohesin_positions_updated_after_step():
    seq, c = make(set(), start_left=50)
    c.step(seq)
    assert seq.cohesin_positions == {49, 51}


def test_cohesin_positions_when_stalled():
    seq, c = make({40, 60}, start_left=41, start_right=59)
    run(c, seq, 5)
    assert seq.cohesin_positions == {41, 59}


# ---------- probabilistic blocking ----------

def test_partial_block_probability_eventually_passes_site():
    # With prob_block=0.5 the right end should get past a site in a
    # reasonable number of steps. Seeded so the result is reproducible.
    random.seed(0)
    seq, c = make({10}, start_left=8, length=1000)
    run(c, seq, 200, prob_block=0.5)
    assert c.position.right > 10


@pytest.mark.parametrize("prob_block", [0.0, 0.5, 1.0])
def test_right_end_never_passes_site_at_prob_one_only(prob_block):
    random.seed(1)
    seq, c = make({10}, start_left=8, length=1000)
    run(c, seq, 100, prob_block=prob_block)
    if prob_block == 1.0:
        assert c.position.right == 9
    else:
        assert c.position.right > 10
