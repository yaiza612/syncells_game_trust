# SynCells Game Trust
Simulation of a synthetic community of cells playing the game of trust. 

## Graphical Description of the model
![Model_scheme](https://user-images.githubusercontent.com/62614099/150428970-bf17a4b1-db3a-4108-8489-32478c4766ed.png)

A: Synthetic Community of five cells playing a game of trust. Each cell produces a QS (quorum signal) but requires the neighbor's QS as well to activate the regulator that allows the transcription of proteins which each cell needs to survive and reproduce. Therefore, in this community every cell shares the QS with their neighbor cell. Nevertheless, sometimes some cells decide being selfish to prosper. B: Mechanism's transcription of the proteins needed for survival and reproduction. Represents an AND GATE; without the five different types of QS, the cell cannot transcribe the proteins.

## Parameters available to play with

*Number of different types of population's cells. (between 2 and 26) 
*Cooperativeness: amount of QS kept, the rest is shared.
*Production: amount of QS produced 
*Step: number of time step to run the simulation
*Size: size of the grid (culture medium)
*Initial density: initial density of cells of every population 
*Cooperation: Percentage of cells of the culture medium are cooperative.
*Threshold survival: Amount of quorum signal the cell need to initiate the transcription of the protein and survive. 
*Threshold reproduction:  Amount of quorum signal the cell need to initiate the transcription of the protein and reproduce. 
*Initial QS: Amount of quorum signal available at the beginning in medium culture or grid.
*Diffusion factor: Amount of quorum signal that diffuses in the medium culture or grid.

## Usage




## Default parameters

| Parameter              | Value |
|------------------------|-------|
| Number of cells        | 5     |
| Cooperativeness        | 0.2   |
| Production             | 1.5   |
| Step                   | 100   |
| Size                   | 20    |
| Initial density        | 0.05  |
| Cooperation            | 0.6   |
| Threshold survival     | 0.4   |
| Threshold reproduction | 0.5   |
| Initial QS             | 1     |
| Diffusion factor       | 0.1   |

## Pricipal Output of the Simulation

In this simulation, the user can see the result of the interactions given the default parameters.

https://user-images.githubusercontent.com/62614099/150420686-5a7adc39-df4e-483d-8661-e2b93adb03cd.mp4

