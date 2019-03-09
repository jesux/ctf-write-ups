# ECSC 2018 - AES 1

```bash
./crypto
crypto - tool to generate keys, encrypt and decrypt

crypto keygen    - generate a new key, displayed as hexstring
crypto enc <key> - encrypt stdin with hexstring key
crypto dec <key> - decrypt stdin with hexstring key
```

```bash
gcc -Wall crypto-bruteforce.c -o crypto-bruteforce -lssl -lcrypto
cat cipher | ./crypto-bruteforce
...
strings out/* -n 20

Swordfish is a 2001 American action crime ...
```

```bash
grep Swordfish out/*

out/4577551_d366288d4490e99553a909c98f7c2947:Swordfish is a 2001 American action crime thriller film directed by Dominic Sena and starring John Travolta, Hugh Jackman, Halle Berry, Don Cheadle, Vinnie Jones and Sam Shepard. The film centers on Stanley Jobson, an ex-con and computer hacker who is targeted for recruitment into a bank robbery conspiracy because of his formidable hacking skills. The film was a slight box office success but was negatively received by critics upon release.
```


```bash
cat cipher | ./crypto dec d366288d4490e99553a909c98f7c2947
```

```
Swordfish is a 2001 American action crime thriller film directed by Dominic Sena and starring John Travolta, Hugh Jackman, Halle Berry, Don Cheadle, Vinnie Jones and Sam Shepard. The film centers on Stanley Jobson, an ex-con and computer hacker who is targeted for recruitment into a bank robbery conspiracy because of his formidable hacking skills. The film was a slight box office success but was negatively received by critics upon release.

Stanley Jobson (Hugh Jackman) is a highly skilled computer hacker. Having served time for infecting the FBI's Carnivore program with a computer virus, he is now on parole but forbidden from using computers. His alcoholic ex-wife Melissa (Drea de Matteo), who married a rich porn producer and is currently a part-time porn actress, has sole custody over their daughter Holly and a restraining order preventing him from visiting their daughter. One day, he is solicited by Ginger Knowles (Halle Berry), speaking for her boss Gabriel Shear (John Travolta), for his hacking skills. He goes to meet Gabriel in Los Angeles, where he is put on the spot to crack a secure government server within a minute while simultaneously held at gunpoint and receiving fellatio. When he succeeds, Gabriel offers Stanley $10 million to program a multi-headed worm, a "hydra", to siphon $9.5 billion from several government slush funds.

Stanley begins work, learning that Gabriel leads Black Cell, a secret group created by J. Edgar Hoover to launch retaliatory attacks against terrorists that threaten the United States. He also privately discovers Ginger is a DEA agent working undercover, and further is surprised to discover a corpse that looks like Gabriel. He goes to see Holly home from school but finds he is being followed by FBI agent J.T. Roberts (Don Cheadle), who had previously caught Stanley. Roberts, though monitoring Stanley closely, is more interested in Gabriel as he does not appear on any government database, and after learning that another hacker, Axl Torvalds (Rudolf Martin), had been killed by Gabriel's men, warns Stanley to be cautious. Stanley opts to secretly code a back door in his hydra that reverses the money transfer after a short period. Meanwhile, Senator Reisman (Sam Shepard), who oversees Black Cell, learns the FBI has started tracking Gabriel and orders him to stand down. Gabriel refuses, and narrowly avoids an assassination attempt ordered by Reisman. Gabriel personally kills Reisman in revenge and continues his plan.

Stanley delivers the hydra to Gabriel and leaves to see Holly, only to find that Gabriel has killed Melissa and her husband and kidnapped Holly, framing Stanley. Stanley has no choice but to participate in the bank heist to get Holly back. Gabriel and his men storm a Worldbanc branch, and secure its employees and customers as hostages, fitting each with ball-bearing-based explosives similar to Claymore mines. When police and FBI surround the branch, Gabriel takes Stanley to the coffee shop across the street to meet with Roberts, but Gabriel spends the time to discuss the film Dog Day Afternoon and the nature of misdirection. Once back in the bank, Gabriel has one of his men escort a hostage to demonstrate the situation. A sniper kills the man, and other agents pull the hostage away from the bank, causing the bomb to detonate, ravaging the buildings and vehicles on the street and killing several people, a scene shown in medias res at the start of the film.

Gabriel instructs Stanley to launch the hydra, and turns Holly over to him once completed. However, Stanley's back door triggers before they can leave the bank, and Stanley is recaptured while Holly is rescued. Gabriel threatens to kill Ginger, who he knows is a DEA agent, unless Stanley re-siphons the money back to a Monte Carlo bank. Despite doing so, Gabriel shoots Ginger. Gabriel and his men load the hostages on a bus and demand a plane wait for them at the local airport, but while en route, the bus is lifted off by a S-64 Aircrane and deposited on the roof of a local skyscraper. Gabriel deactivates the bombs and departs with his surviving men on a waiting helicopter, which Stanley shoots down using a rocket-propelled grenade from the bus.

Roberts takes Stanley to verify the corpse they found, believing Gabriel was a Mossad agent while there was no record of a DEA agent named Ginger. Stanley recognizes the corpse as the one he discovered earlier and personally realizes that the whole scenario was misdirection. The Police still cannot find Ginger's corpse. Gabriel had escaped a different route, and Ginger had been wearing a bulletproof vest and was working with Gabriel all along. Stanley does not tell Police that Gabriel & Ginger are still alive. Roberts arranges for Stanley to have full custody of Holly, and the two tour the US together. In Monte Carlo, Gabriel and Ginger withdraw the money, and later watch as a yacht at sea explodes. Over the film's credits, a news report describes the destruction of the yacht, carrying a known terrorist, as the third such incident in as many weeks.

https://en.wikipedia.org/wiki/Swordfish_(film)
```
