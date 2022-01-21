# SynCells Game Trust
Simulation of a synthetic community of cells playing the game of trust. 

## Graphical Description of the model
![Model_scheme](https://user-images.githubusercontent.com/62614099/150428970-bf17a4b1-db3a-4108-8489-32478c4766ed.png)

A: Synthetic Community of five cells playing a game of trust. Each cell produces a QS (quorum signal) but requires the neighbor's QS as well to activate the regulator that allows the transcription of proteins which each cell needs to survive and reproduce. Therefore, in this community every cell shares the QS with their neighbor cell. Nevertheless, sometimes some cells decide being selfish to prosper. B: Mechanism's transcription of the proteins needed for survival and reproduction. Represents an AND GATE; without the five different types of QS, the cell cannot transcribe the proteins.

## Usage

`python main.py`

## Parameters available to play with

* Number of different types of population's cells. (between 2 and 26) `-num`
* Cooperativeness: amount of QS kept, the rest is shared. `-co`
* Production: amount of QS produced  `-prod`
* Step: number of time step to run the simulation `-s`
* Size: size of the grid (culture medium) `-n`
* Initial density: initial density of cells of every population  `-d`
* Cooperation: Percentage of cells of the culture medium are cooperative. `-c`
* Threshold survival: Amount of quorum signal the cell need to initiate the transcription of the protein and survive.  `-ts`
* Threshold reproduction:  Amount of quorum signal the cell need to initiate the transcription of the protein and reproduce. `-tr`
* Initial QS: Amount of quorum signal available at the beginning in medium culture or grid. `-i`
* Diffusion factor: Amount of quorum signal that diffuses in the medium culture or grid. `-f`

## Additional parameters

* Path images simulation `-pis`
* Path additional figures `-pa`
* Name of the video `-v`

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

## Principal Output of the Simulation

In this simulation, the user can see the result of the interactions given the default parameters.


https://user-images.githubusercontent.com/62614099/150576616-c9ac14fc-3919-4f1a-b44c-0bb5346d7225.mp4


## Aditional Outputs 

![cells](https://user-images.githubusercontent.com/62614099/150576714-02ad9285-330a-47fa-92fe-70c1cb0572d5.png)
![selfish](https://user-images.githubusercontent.com/62614099/150576722-63660422-7fd5-4854-8c2a-b4553e194c6e.png)
![quorum_signals](https://user-images.githubusercontent.com/62614099/150576718-cb1d8c85-7191-4e44-ab9e-5e94bd70740b.png)
![savings](https://user-images.githubusercontent.com/62614099/150576720-dbfa1d84-398c-4e23-b8e2-b2b09c02cbe4.png)


