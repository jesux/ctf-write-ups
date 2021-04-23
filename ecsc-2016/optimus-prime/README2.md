# OPTIMUS PRIME 2

```
-----BEGIN RSA PRIVATE KEY-----
MIIG4wIBAAKCAYEAnq48eqHsUugZkz4rFqROVvPa9fvxqoJx6b81MuigBe9ANavd
YYNCrN8zryxHBo+l2Z0EkA11p1mF/swa0SFUfYnUsuZpfqjDvELrsWf+jmtxRrk4
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************AoHBANAiZPCv9AHjyhOJOBJBu1Ul1B0PPaBk
****************************************************************
****************************************************************
****************************************************************
********************************nQKBwQDDLFM+elj7PMd3hCd1Mv61OppQ
Fr9UNQ94zQ8XBba008u7UDrS2VaVxrT3jpCPTQvklqnZqN4aJnBII6Seb/2Io99M
7TA/ByqgxSnRst+M1F+xR68ghHOr6GKPO6oxc2abYZkIKd9LoERZjgXId9P+Y0GN
QHkUMhWFTOUh05hJLA+quaKxP+cylQMVFgLxWMql2wJ5aiR9MIkqovpugMBdKNiq
SoZclykLs2ZD1WtrC5zSN26ZDmm9yxMs3xi5ip8CgcBgt3rcdYcX0bg3d848fZsF
qDx2/HwQqmS5m25ufy31PJshUIyvw2u9NBVnnItVGSrdB1MvMDJFoSVpJVGx/6A2
eMsXp3UWIZwxc2yWYc/VHb0ACmuuF3VRR4cj4o6ZeEn+n6yRSIWry05bRTi7OdZg
J0412cx0EwA2qqc95HuHqLBOQ+Hd+UExj9q7MQKGJHa3iGdaxiHVMKeThD55qiiX
QeRick+jH6EKfU/dYg5/fqgug4C1TDlZovZY3R5n2+kCgcBShmiAb302ZkG1QHTq
snBOswPSv3uRIIp1OseZpXnWxgNMJaVpyCo7VHTqhCaN4TcZJbeV6DhZeE1bw250
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************
-----END RSA PRIVATE KEY-----
```
### Extract ASN.1 values
```
=== Beginning of n ===
02820181
009eae3c7aa1ec52e819933e2b16a44e56f3daf5fbf1aa8271e9bf3532e8a005ef4035abdd618342acdf33af2c47068fa5d99d04900d75a75985fecc1ad121547d89d4b2e6697ea8c3bc42ebb167fe8e6b7146b938

=== Beginning of p ===
0281c1
00d02264f0aff401e3ca1389381241bb5525d41d0f3da064
=== Ending of p === 
9d
=== q ===
0281c1
00c32c533e7a58fb3cc77784277532feb53a9a5016bf54350f78cd0f1705b6b4d3cbbb503ad2d95695c6b4f78e908f4d0be496a9d9a8de1a26704823a49e6ffd88a3df4ced303f072aa0c529d1b2df8cd45fb147af208473abe8628f3baa3173669b61990829df4ba044598e05c877d3fe63418d4079143215854ce521d398492c0faab9a2b13fe7329503151602f158caa5db02796a247d30892aa2fa6e80c05d28d8aa4a865c97290bb36643d56b6b0b9cd2376e990e69bdcb132cdf18b98a9f

=== dp ===
0281c0
60b77adc758717d1b83777ce3c7d9b05a83c76fc7c10aa64b99b6e6e7f2df53c9b21508cafc36bbd3415679c8b55192add07532f303245a125692551b1ffa03678cb17a77516219c31736c9661cfd51dbd000a6bae177551478723e28e997849fe9fac914885abcb4e5b4538bb39d660274e35d9cc74130036aaa73de47b87a8b04e43e1ddf941318fdabb3102862476b788675ac621d530a793843e79aa289741e462724fa31fa10a7d4fdd620e7f7ea82e8380b54c3959a2f658dd1e67dbe9

=== Beginning of dq ===
0281c0
528668806f7d366641b54074eab2704eb303d2bf7b91208a753ac799a579d6c6034c25a569c82a3b5474ea84268de1371925b795e83859784d5bc36e74
```

### Resolv
```python
def recover_parameters(q, dp, e, nFirst, pFirst):
    d1p = dp * e - 1
    for k in range(3, e):
      if d1p % k == 0:
        hp = d1p // k
        p = hp + 1
        if pFirst in hex(p):
          print('[+] Found possible P: %x' % p)
          if nFirst in hex(p*q):
            return(p, q)


q = 0x00c32c533e7a58fb3cc77784277532feb53a9a5016bf54350f78cd0f1705b6b4d3cbbb503ad2d95695c6b4f78e908f4d0be496a9d9a8de1a26704823a49e6ffd88a3df4ced303f072aa0c529d1b2df8cd45fb147af208473abe8628f3baa3173669b61990829df4ba044598e05c877d3fe63418d4079143215854ce521d398492c0faab9a2b13fe7329503151602f158caa5db02796a247d30892aa2fa6e80c05d28d8aa4a865c97290bb36643d56b6b0b9cd2376e990e69bdcb132cdf18b98a9f
dp = 0x60b77adc758717d1b83777ce3c7d9b05a83c76fc7c10aa64b99b6e6e7f2df53c9b21508cafc36bbd3415679c8b55192add07532f303245a125692551b1ffa03678cb17a77516219c31736c9661cfd51dbd000a6bae177551478723e28e997849fe9fac914885abcb4e5b4538bb39d660274e35d9cc74130036aaa73de47b87a8b04e43e1ddf941318fdabb3102862476b788675ac621d530a793843e79aa289741e462724fa31fa10a7d4fdd620e7f7ea82e8380b54c3959a2f658dd1e67dbe9
e = 0x10001
nFirst = '9eae3c7aa1ec52e819933e2b16a44e56f3daf5fbf1aa8271e9bf3532e8a005ef4035abdd618342acdf33af2c47068fa5d99d04900d75a75985fecc1ad121547d89d4b2e6697ea8c3bc42ebb167fe8e6b7146b938'
pFirst = 'd02264f0aff401e3ca1389381241bb5525d41d0f3da064'

p, q = recover_parameters(q, dp, e, nFirst, pFirst)
print("p: %lu" % p)
print("q: %lu" % q)
```

### Private Key

```
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
```

### Links
* <https://github.com/Ganapati/RsaCtfTool/blob/master/attacks/single_key/partial_q.py>
* https://lapo.it/asn1js/
