from pyechonext.security.hashing import (HashAlgorithm, PlainHasher,
                                         SaltedHasher)

hasher = PlainHasher(HashAlgorithm.BLAKE2S)
old_hash = hasher.hash("TEXT")
new_hash = hasher.hash("TEXT")

if hasher.verify("TEXT", new_hash):  # true
    print("Yes!")

if hasher.verify("TEXT2", old_hash):  # false
    print("Yes!")


hasher = SaltedHasher(HashAlgorithm.BLAKE2S, salt="bob")
old_hash = hasher.hash("TEXT")
new_hash = hasher.hash("TEXT")

if hasher.verify("TEXT", new_hash):  # true
    print("Yes!")

if hasher.verify("TEXT2", old_hash):  # false
    print("Yes!")
