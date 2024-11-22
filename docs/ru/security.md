# pyEchoNext / Безопасность

---

Безопасности в pyEchoNext уделяется особое внимание. Мы понимаем, что некоторые разработчики могут пренебрегать базовой защитой от уязвимостей, и поэтому позаботились об системе предупреждений, криптографии и защите от внешних угроз.

## Хеширование
Хеширование - процесс преобразования данных в уникальную строку фиксированной длины.

В нашей библиотеке поддерживается базовое хеширование через PlainHasher и SaltedHasher. SaltedHasher - модифицированная версия обычного, где к хешу добавляется "соль". То есть строка "Hello" при соли "bob" превращается в "bobHello". Это помогает избавиться от хеш-коллизий (момент, когда хеши двух разных строк совпадают). Хеширование обычно используют для хранения важных данных: например, паролей.

### pyechonext.security.hashing
Модуль, отвечающий за хеширование.

#### Hash-Algorithm
Enum-класс хеш-алгоритма. Поддерживается SHA256, SHA512, MD5, BLAKE2B, BLAKE2S.

```python
class HashAlgorithm(Enum):
	"""
	This class describes a hash algorithms.
	"""

	SHA256 = auto()
	SHA512 = auto()
	MD5 = auto()
	BLAKE2B = auto()
	BLAKE2S = auto()
```

#### PlainHasher
Простой класс для хеширования:

```python
from pyechonext.security.hashing import HashAlgorithm, PlainHasher

hasher = PlainHasher(HashAlgorithm.BLAKE2S)
old_hash = hasher.hash("TEXT")
new_hash = hasher.hash("TEXT")

if hasher.verify("TEXT", new_hash): # true
    print('Yes!')

if hasher.verify("TEXT2", old_hash): # false
    print('Yes!')

# Output: one "Yes!"
```

#### SaltedHasher
Класс для хеширования с солью:

```python
from pyechonext.security.hashing import HashAlgorithm, SaltedHasher

hasher = SaltedHasher(HashAlgorithm.BLAKE2S, salt='bob')
old_hash = hasher.hash("TEXT")
new_hash = hasher.hash("TEXT")

if hasher.verify("TEXT", new_hash): # true
    print('Yes!')

if hasher.verify("TEXT2", old_hash): # false
    print('Yes!')

# Output: one "Yes!"
```

### pyechonext.security.crypts
Модуль с различными вещами для шифрования и криптографии:

#### PSPCAlgorithm
Point Simple Password Crypt Algorithm - Точечный Простой Алгоритм Шифрования Паролей (ТПАШП).

```
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
```

Пример:

```python
from pyechonext.security.crypts import PSPCAlgorithm


pspc = PSPCAlgorithm()

passwords = ['AngryPassword', 'S0mesd7623tds@&6^@_', 'PassWord', 'Pass']

for password in passwords:
    print('Base:', password)
    print('Crypted:', pspc.crypt(password))
    print('Decrypted:', pspc.decrypt(pspc.crypt(password)))
    print()
```

---

[Содержание](./index.md)

