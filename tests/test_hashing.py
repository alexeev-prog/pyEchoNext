from pyechonext.security.hashing import HashAlgorithm, PlainHasher, SaltedHasher


def test_plain_hasher():
	hasher = PlainHasher(HashAlgorithm.BLAKE2S)
	old_hash = hasher.hash("TEXT")
	new_hash = hasher.hash("TEXT")

	assert hasher.verify("TEXT", new_hash)
	assert not hasher.verify("TEXT2", old_hash)


def test_salted_hasher():
	hasher = SaltedHasher(HashAlgorithm.BLAKE2S, salt="bob")
	old_hash = hasher.hash("TEXT")
	new_hash = hasher.hash("TEXT")

	assert hasher.verify("TEXT", new_hash)
	assert not hasher.verify("TEXT2", old_hash)
