# Machine-Learning-Cells

A Cell generation lives for 45 seconds.

Here is a small explanation of the features of the Cell class(such as size parameters etc)

- the size of a cell is the surface area of a cell in pixels.

- the activity radius of a cell is an ellipse that has its corresponding rectangle's dimensions proportional to the bounding rectangle of the Cell shape(each dimension is 2.5 times the one of the Cell).

- the regular speed of a cell is 100 pixels / second. The speed parameter represents a factor by which the regular speed is multiplied and is determined in a pseudo random way.  
the formula for speed is as follows:   
![speed eq](https://user-images.githubusercontent.com/38582034/65237132-aeb3e500-dae2-11e9-907b-8667d4e104df.png)

- the hunger is a value between 0 and 1 that represents an encoding for the time a cell has left until it dies; it is continously decreasing and, the lower it gets, the faster the cell is. the encoding represents the percentage of the initial 20 seconds of lifetime left(1 being 100% and 0 being 0%). The initial time can be affected by the random speed factor, however the percentage works in the same way(obviously).

- the kills variable stores the number of cells killed by the respective cell.

- the algae variable stores how many algae the respective cell ate.

- the seconds alive variable is self explanatory

- the survivability is the fitness score of a cell. it is calculated by the following formula:  
![SV formula](https://user-images.githubusercontent.com/38582034/65237806-099a0c00-dae4-11e9-8ccd-bb40c4e05ef4.png)

- the food preference is a variable that takes a value between 0 and 1 and represents exactly what its name says: whether a cell prefers algae or other cells. there are two types of food preferences: the _initial_ and the _actual_ food preference of a cell. The _initial_ food preference is set at 0.5 and is affected by previous generations and random mutations, while the _actual_ food preference is calculated based on what the cell ate while it was alive. The _actual_ food preference of a cell is used for future generations for determining their _initial_ food preference.
