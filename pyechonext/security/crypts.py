from random import randint


def get_seed(seed: int, min_n: int = 1, max_n: int = 1000) -> int:
    """
    Gets the seed.

    :param		seed:  The number
    :type		seed:  int

    :returns:	The seed.
    :rtype:		int
    """
    if seed is None:
        return randint(min_n, max_n)
    else:
        return seed


class PSPCAlgorithm:
    """
    This class describes a pspc algorithm (Point Simple Password Crypt
    Algorithm)
    """

    def __init__(self, seed: int = None):
        """
        Constructs a new instance.

        :param		seed:  The seed
        :type		seed:  int
        """
        self.seed = get_seed(seed)

    def crypt(self, password: str) -> str:
        """
        Crypt password

        :param		password:  The password
        :type		password:  str
        :param		seed:	   The seed
        :type		seed:	   int

        :returns:	crypted password
        :rtype:		str
        """
        if not password:
            return ""

        crypted = " ".join(password).split()
        crypted = list(map(ord, crypted))

        return ".".join(list(map(lambda x: str(x * self.seed), crypted)))[::-1]

    def decrypt(self, crypted: str) -> str:
        """
        Decrypt password

        :param		crypted:  The crypted
        :type		crypted:  str

        :returns:	decrypted value
        :rtype:		str
        """
        if not crypted:
            return ""

        password = list(map(lambda x: int(x) // self.seed,
                        crypted[::-1].split(".")))
        return "".join(list(map(chr, password)))
