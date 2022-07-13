import wget
URL = "http://ohpdmc.eri.u-tokyo.ac.jp/pub3/breq-fast-nm/D20220713040632-194-16/NM1201102080000.seed"
response = wget.download(URL, "seedFile/NM1201102080000.seed")