from pyechonext.security.crypts import PSPCAlgorithm


pspc = PSPCAlgorithm()

passwords = ['AngryPassword', 'S0mesd7623tds@&6^@_', 'PassWord', 'Pass']

for password in passwords:
	print('Base:', password)
	print('Crypted:', pspc.crypt(password))
	print('Decrypted:', pspc.decrypt(pspc.crypt(password)))
	print()
