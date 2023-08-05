# matrix_path


## Description
Use the matrix class to create matrix objects and navigate the 2D matrix. Move with the ``` right ```, ``` left ```, ``` up ```, and ``` down ``` functions.
The '1's represent the path.

## Installation 
```pip install matrix_path```

## How to use?
```
from matrix import Matrix

start_point = [0, 0]
end_point = [0, 4]
walls = [[0, 1], [1, 2]]
maze = Matrix(5, start_point, end_point, walls)
maze.print_matrix()
```

## License
© 2020 Arush Sharma

This repository is licensed under the MIT license. See LICENSE for details.