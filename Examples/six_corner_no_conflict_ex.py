def get_six_corner_adjacent_perfect_filtration():
    filtration = [[3], [4], [0], [1], [2], [5],
                  [3, 4], [0, 4], [0, 3],
                  [1, 2], [1, 5], [2, 5],
                  [1, 4],
                  [4, 5], [0, 1],
                  [0, 3, 4], [1, 2, 5], [1, 4, 5], [0, 1, 4]
                  ]
    return filtration
