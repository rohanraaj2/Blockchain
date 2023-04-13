import hashlib
import time

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = []

    def create_tree(self):
        level = self.transactions
        while len(level) > 1:
            new_level = []
            for i in range(0, len(level), 2):
                if i == len(level) - 1:
                    new_level.append(self.hash(level[i]))
                else:
                    new_level.append(self.hash(level[i] + level[i+1]))
            self.tree.append(new_level)
            level = new_level
        return self.tree[-1][0]

    def hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        return f"{self.sender}->{self.receiver}:{self.amount}"

class Block:
    def __init__(self, transactions, prev_hash):
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.merkle_root = MerkleTree([str(tx) for tx in transactions]).create_tree()
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        data = f"{self.timestamp}{self.merkle_root}{self.prev_hash}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty):
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.genesis_block()]
        self.difficulty = difficulty

    def genesis_block(self):
        return Block([Transaction("genesis", "genesis", 0)], "0")

    def add_block(self, transactions):
        prev_hash = self.chain[-1].hash
        block = Block(transactions, prev_hash)
        block.mine(self.difficulty)
        self.chain.append(block)

# Sample usage
if __name__ == "__main__":
    blockchain = Blockchain()
    transactions = [Transaction("A", "B", 10), Transaction("B", "C", 20)]
    blockchain.add_block(transactions)
    transactions = [Transaction("C", "A", 5), Transaction("A", "D", 30)]
    blockchain.add_block(transactions)

    for block in blockchain.chain:
        print(f"Block {blockchain.chain.index(block)}: {block.hash}")
This code example provides a minimal blockchain with a Merkle tree for securing transaction data within each block. The Merkle tree is generated from the transaction data, and the root of the tree is stored in the block. The blockchain is then mined with a simple proof-of-work algorithm.

Keep in mind that this example is not suitable for real-world applications, as it lacks many essential features, such as a proper consensus algorithm, a network protocol, error handling, and performance optimizations.
