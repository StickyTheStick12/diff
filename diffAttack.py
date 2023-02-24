from SPN import Encrypt
from SPN import Keygen
import attack

key = Keygen(True)

# generate our cipher pairs
cipherPair = []
plainTextDiff = 0b10110000

for plaintextOne in range(2000): # limit how many plaintexts we will generate to make the bruteforce faster
    cipherOne = Encrypt(plaintextOne, key)
    plainTextTwo = plaintextOne ^ plainTextDiff
    cipherTwo = Encrypt(plainTextTwo, key)
    cipherPair.append([cipherOne, cipherTwo])


char = {2: [2, 4], 4: [2, 4]}

hits = attack.GetHits(cipherPair, char)

bestKey = 0
biggestHit = 0

for key, hit in enumerate(hits):
    if hit > biggestHit:
        biggestHit = hit
        bestKey = key

print("\nFound the following key parts")
temp = str(bin(bestKey)[2:]).zfill(8)
print(f"Block 2: {temp[0:4]}, {hex(int(temp[0:4], 2))[2:]}")
print(f"Block 4: {temp[4:]}, {hex(int(temp[4:], 2))[2:]}")
