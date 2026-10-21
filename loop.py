from dataclass import Sequence, OrderedPair, Cohesin
import random
from visualization import plot_arcs

def loop(cohesins, seq, time):
    """
    Simulates cohesin loop creation on a "sequence".

    Args:
        cohesins: list of Cohesin objects
        seq: Sequence object
        time: number of steps for simulation to run on
    Returns:
        snapshot_list: a list of lists containing tuples of current cohesin positions
        loop_sizes: a list of all loop finalized in a simulation     
    """
    snapshot_list = []
    loop_sizes = []
    for s in range(time):
        for c in cohesins:
            if not c.bound:
                c.bind(seq)
            else:
                c.step(seq)
                if random.random() <= seq.detachment_chance:
                    c.detach(seq)
                    loop_sizes.append(c.loop_size())
        if s % 10 == 0:
            snapshot_list.append(snapshot(cohesins))
    return snapshot_list, loop_sizes
    

def snapshot(cohesins):
    """
    Saves current cohesin positions in a list.
    
    Args:
        cohesins: list of cohesin objects.
    Returns:
        snapshots: list of tuples with current cohesin positions 
    
    """
    snapshots: list[tuple] = list()
    for c in cohesins:
        snapshots.append((c.position.left, c.position.right))
    return snapshots


def main():
    ctcf_sites = {2000, 2500, 6000}
    seq = Sequence(length = 10000, ctcf_positions=ctcf_sites)
    cohesins = [Cohesin(position = OrderedPair(-1, -1))]
    time = 10000
    snapshots, loop_sizes = loop(cohesins, seq, time)
    print(loop_sizes)
    print(sum(loop_sizes)/len(loop_sizes))

    plot_arcs([(1209, 1400), (4600, 4800), (3400, 3500)])

if __name__ == "__main__":
    main()
