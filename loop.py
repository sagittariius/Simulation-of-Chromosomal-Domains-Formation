from dataclass import Sequence, OrderedPair, Cohesin, ContactMap
import random
import visualization as viz


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
        if c.bound:
            snapshots.append((c.position.left, c.position.right))
    return snapshots

def build_contact_map(seq, snapshots, bin_width=10):
    """
    Builds a ContactMap from saved snapshots. 

    Args:
        seq: Sequence object
        snapshots: list returned by loop()
        bin_width: number of sequence positions per bin
    Returns:
        The filled ContactMap.
    """
    contact = ContactMap(sequence=seq, bin_width=bin_width)

    for loops in snapshots:
        contact.add_snapshot(loops)

    return contact


def main():
    #ctcf_sites = {600, 1300, 2200}
    ctcf_sites = {2000, 2500, 6000}
    seq = Sequence(length = 10000, ctcf_positions=ctcf_sites)
    num_cohesins = 15 # about one every 200 positions, like in the paper
    cohesins = [Cohesin(position = OrderedPair(-1, -1)) for _ in range(num_cohesins)]
    #cohesins = [Cohesin(position = OrderedPair(-1, -1))]
    time = 20000
    snapshots, loop_sizes = loop(cohesins, seq, time)
    contact_map = build_contact_map(seq, snapshots, bin_width=30)

    print(loop_sizes)
    print(sum(loop_sizes)/len(loop_sizes)) 

    # Visualizations (saved as PNG files)
    viz.plot_contact_matrix(contact_map.observed_over_expected(), seq.length, seq.ctcf_positions,
                        title="Simulated contact map",
                        cmap="YlOrRd").savefig("contact_map.png", dpi=150)
    
if __name__ == "__main__":
    main()
