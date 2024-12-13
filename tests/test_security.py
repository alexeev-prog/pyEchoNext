from pyechonext.security.crypts import PSPCAlgorithm


def test_security():
	pspc = PSPCAlgorithm(100)

	passwords = ["AngryPassword", "S0mesd7623tds@&6^@_", "PassWord", "Pass"]

	assert (
		pspc.crypt(passwords[0])
		== "00001.00411.00111.00911.00511.00511.0079.0008.00121.00411.00301.00011.0056"
	)
	assert (
		pspc.crypt(passwords[1])
		== "0059.0046.0049.0045.0083.0046.00511.00001.00611.0015.0005.0045.0055.00001.00511.00101.00901.0084.0038"
	)
	assert pspc.crypt(passwords[2]) == "00001.00411.00111.0078.00511.00511.0079.0008"
	assert pspc.crypt(passwords[3]) == "00511.00511.0079.0008"

	assert pspc.decrypt(pspc.crypt(passwords[0])) == passwords[0]
	assert pspc.decrypt(pspc.crypt(passwords[1])) == passwords[1]
	assert pspc.decrypt(pspc.crypt(passwords[2])) == passwords[2]
	assert pspc.decrypt(pspc.crypt(passwords[3])) == passwords[3]
