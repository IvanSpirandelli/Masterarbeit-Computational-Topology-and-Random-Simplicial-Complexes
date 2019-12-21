
filename = "Datasets/xqf131"
with open(filename, 'r') as data:
    lines = data.readlines()[8:-1]

    points = [[int(y.split(" ")[1]), int(y.split(" ")[2])] for y in [x.strip() for x in lines]]
    print(points)

