# Machine-Learning-Cells
self explanatory

Here is a small explanation of the features of the Cell class(such as size parameters etc)

- the size of a cell is the surface area of a cell in pixels.

- the regular speed of a cell is 100 pixels / second. The speed parameter represents a factor by which the regular speed is multiplied and is determined in a pseudo random way.  
the formula for speed is as follows:   
![speed eq](https://user-images.githubusercontent.com/38582034/65237132-aeb3e500-dae2-11e9-907b-8667d4e104df.png)

- the hunger is a value between 0 and 1 that represents an encoding for the time a cell has left until it dies; it is continously decreasing and, the lower it gets, the faster the cell is. the encoding represents the percentage of the initial 20 seconds of lifetime left(1 being 100% and 0 being 0%). The initial time can be affected by the random speed factor, however the percentage works in the same way(obviously).

