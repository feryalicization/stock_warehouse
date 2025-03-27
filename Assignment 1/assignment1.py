class LFSR:
    def __init__(self, state: str, taps: list):
        self.state = [int(bit) for bit in state] 
        self.taps = taps
        self.n = len(state)
    
    def get_state(self):
        return ''.join(map(str, self.state))
    
    def next_bit(self):
        feedback = 0
        for tap in self.taps:
            feedback ^= self.state[tap]
        
        next_output = self.state[-1]  
        
        self.state = [feedback] + self.state[:-1]
        
        return next_output
    
    def reset(self, new_state: str):
        """Resets the LFSR to a new state."""
        self.state = [int(bit) for bit in new_state]

def basic_lfsr():
    lfsr = LFSR(state='0110', taps=[3, 2]) 
    print("Basic LFSR Output:")
    for _ in range(20):
        print(f"State: {lfsr.get_state()}, Output bit: {lfsr.next_bit()}")
        
def test_general_lfsr():
    general_lfsr = LFSR(state='0110', taps=[3, 2]) 
    print("\nGeneral LFSR Output:")
    for _ in range(20):
        print(f"State: {general_lfsr.get_state()}, Output bit: {general_lfsr.next_bit()}")

if __name__ == "__main__":
    basic_lfsr()
    test_general_lfsr()
