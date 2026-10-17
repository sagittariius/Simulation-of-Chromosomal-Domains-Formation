from dataclasses import dataclass, field
import random

@dataclass
class OrderedPair:
    # I'm not sure we need it, but for now it is like this
    left: int
    right: int

@dataclass
class Cohesin:
    # position is coordinates of 2 sequence positions inside the cohesin ring currently
    position: OrderedPair
    bound: bool = False

    def loop_size(self):
        # Calculates the loop size
        return self.position.right - self.position.left

    def step(self, seq, prob_block=1.0):
        # Remove the old loop end positions from the sequence
        seq.cohesin_positions.discard(self.position.left)
        seq.cohesin_positions.discard(self.position.right)
        
        # Attempt movement of right loop end one position to the right
        move_right = self.position.right + 1
        if move_right < seq.length:
            # Check for CTCF position and block probability
            blocked = (
                move_right in seq.ctcf_positions and random.random() < prob_block
            )
            if not blocked:
                self.position.right = move_right


        # Attempt movement of left loop end one posisiont to the left
        move_left = self.position.left -1
        if move_left >= 0:
            # Check for CTCF position and block probability
            blocked = (
                move_left in seq.ctcf_positions and random.random() < prob_block
            )
            if not blocked:
                self.position.left = move_left

        # Updates current positions on the sequence
        seq.cohesin_positions.add(self.position.left)
        seq.cohesin_positions.add(self.position.right)

    def bind(self, seq):
        # Attaches cohesin
        self.bound = True
        spot = seq.pick_spot()  
        self.position.left = spot
        self.position.right = spot
        seq.cohesin_positions.add(spot)

    def detach(self, seq):
        # Detaches cohesin
        self.bound = False
        seq.cohesin_positions.discard(self.position.left)
        seq.cohesin_positions.discard(self.position.right)


@dataclass 
class Sequence:
    length: int = 1000
    detachment_chance: float = 0.01
    ctcf_positions: set[int] = field(default_factory=set)
    cohesin_positions: set[int] = field(default_factory=set)

    def pick_spot(self):
        # Randomly pickes a place for attachment
        # Later can be improved by adding weights to certain locations
        spot = random.randint(0, self.length-1)
        while spot in self.cohesin_positions:
            spot = random.randint(0, self.length-1)
        return spot
