Security
===========================================

--------------

Security is a top priority at pyEchoNext. We understand that some
developers may neglect basic protection against vulnerabilities, and
therefore we took care of the warning system, cryptography and
protection against external threats.

Hashing
-------

Hashing is the process of converting data into a unique string of a
fixed length.

Our library supports basic hashing via PlainHasher and SaltedHasher.
SaltedHasher is a modified version of the usual one, where “salt” is
added to the hash. That is, the string “Hello” with the salt “bob” turns
into “bobHello”. This helps get rid of hash collisions (the moment when
the hashes of two different strings match). Hashing is usually used to
store sensitive data, such as passwords.

pyechonext.security.hashing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Module responsible for hashing.

Hash-Algorithm
^^^^^^^^^^^^^^

Enum class of hash algorithm. SHA256, SHA512, MD5, BLAKE2B, BLAKE2S are
supported.

.. code:: python

   class HashAlgorithm(Enum):
      """
      This class describes a hash algorithms.
      """

      SHA256 = auto()
      SHA512 = auto()
      MD5 = auto()
      BLAKE2B = auto()
      BLAKE2S = auto()

PlainHasher
^^^^^^^^^^^

A simple class for hashing:

.. code:: python

   from pyechonext.security.hashing import HashAlgorithm, PlainHasher

   hasher = PlainHasher(HashAlgorithm.BLAKE2S)
   old_hash = hasher.hash("TEXT")
   new_hash = hasher.hash("TEXT")

   if hasher.verify("TEXT", new_hash): # true
      print('Yes!')

   if hasher.verify("TEXT2", old_hash): # false
      print('Yes!')

   # Output: one "Yes!"

SaltedHasher
^^^^^^^^^^^^

Class for hashing with salt:

.. code:: python

   from pyechonext.security.hashing import HashAlgorithm, SaltedHasher

   hasher = SaltedHasher(HashAlgorithm.BLAKE2S, salt='bob')
   old_hash = hasher.hash("TEXT")
   new_hash = hasher.hash("TEXT")

   if hasher.verify("TEXT", new_hash): # true
      print('Yes!')

   if hasher.verify("TEXT2", old_hash): # false
      print('Yes!')

   # Output: one "Yes!"

pyechonext.security.crypts
~~~~~~~~~~~~~~~~~~~~~~~~~~

Module with various things for encryption and cryptography:

PSPCAlgorithm
^^^^^^^^^^^^^

Point Simple Password Crypt Algorithm - Point Simple Password Encryption
Algorithm (TPASP).

::

   Base: AngryPassword
   Crypted: 00778.87999.74379.363401.558001.558001.96058.06107.711601.87999.13309.07469.50075
   Decrypted: AngryPassword

   Base: S0mesd7623tds@&6^@_
   Crypted: 51338.82165.83428.85374.62333.82165.558001.00778.237101.72744.05834.85374.53284.00778.558001.77588.39559.69024.19727
   Decrypted: S0mesd7623tds@&6^@_

   Base: PassWord
   Crypted: 00778.87999.74379.99267.558001.558001.96058.06107
   Decrypted: PassWord

   Base: Pass
   Crypted: 558001.558001.96058.06107
   Decrypted: Pass

Example:

.. code:: python

   from pyechonext.security.crypts import PSPCAlgorithm


   pspc = PSPCAlgorithm()

   passwords = ['AngryPassword', 'S0mesd7623tds@&6^@_', 'PassWord', 'Pass']

   for password in passwords:
      print('Base:', password)
      print('Crypted:', pspc.crypt(password))
      print('Decrypted:', pspc.decrypt(pspc.crypt(password)))
      print()

--------------
