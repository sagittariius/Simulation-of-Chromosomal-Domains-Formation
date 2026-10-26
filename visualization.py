import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def plot_contact_matrix(matrix, seq_length, ctcf_positions = None,
                        title="Contact map", label="Contact probability",
                        cmap="YlOrRd"):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(matrix, cmap=cmap, origin="upper", extent=[0, seq_length, seq_length, 0])
    fig.colorbar(im, ax=ax, label=label)
    for p in (ctcf_positions or []):
        ax.axvline(p, color="tab:blue", linewidth=0.8, alpha=0.7)
        ax.axhline(p, color="tab:blue", linewidth=0.8, alpha=0.7)
    ax.set_xlabel("Position on sequence")
    ax.set_ylabel("Position on sequence")
    ax.set_title(title)
    fig.tight_layout()
    return fig
                            
def plot_arcs():
    # Needs implementation
    # I thought about plotting an arch of a loop on the sequence as Fig S2 diagram.
    return
