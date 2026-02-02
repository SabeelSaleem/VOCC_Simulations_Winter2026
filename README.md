# VOCC_Simulations_Winter2026

Readme being updated as project progresses.

## Naphthalene On Glass

First Naphthalene on a crystalline SiO2 substrate was modelled to attempt to run in QuantumEspresso. However after further consideration, a perfectly crystalline SiO2 substrate would be too ideal for adsorption study.

## Amorphous Borosilicate Modelling Using Classical Molecular Dynamics

To simulate a more accurate glass substrate (lab glass found in typical laboratory environments for testing and experiments) a Boro-aluminosilicate glass was chosen as substrate of choice. Specifically 3.3 Expansion Borosilicate Glass, composition of which is readily found online. Compsition chosen to be modelled included matrix borosilicate with Na and Al dopants amongst the Borosilicate. Using the LAMMPS package, the initial plan was to utilize the Reaxff model for Force Field based simulation however due to the difficulty in finding proper Reaxff parameters in relevant literature and lack of funding for proper tools (Amsterdam Modeling Suite) to combine parameters from separate literatures in order to create proper parameters, the short range Buckingham/ long range Coulomb atomic pair model was chosen instead due to relevant literature and parameters available at the time of modelling. The melt-quench process as outlined in Deng and Du's paper was followed along with their parameters yielding a cubic amorphous boroaluminosilicate glass cube of ~4185 atoms for future use. 

## Final Goal of Project

Using AIMD methodology, simulate desorption process to yield Energy curve and using K2-SURF models, calculate relevant desiarable variables.

- k<sub>D</sub> Desorption Rate Constant (s<sup>-1</sup> Using the K2-SURF Arrhenius Equation)
- k<sub>A</sub> Adsorption Rate Constant (This is found using published values of the Henry's Law Constant of various PAHs and VOCs with Simulated values of k<sub>D</sub>)
- Predictive Persistence Lifetime (Found through data mapping of simulated energies to experimentally known persistence lifetimes of experimentally tested VOCs and applying model to untested VOCs through simulation.)
