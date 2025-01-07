import drawsvg as draw
import os
import numpy as np

zero_vec =(0,0)
direcs =  [(1,0), (2.1,1), (0.89, 1.0), (1, 2.04), (0,1), (-1.022, 1.997), (-1.07, 1.05), (-2.002, 1.08)]

direcs =  [(1,0), (2,1), (1,1), (0,1)]
direcs =  [(1,0), (2,1), (1,1), (0,1), (1,-1)]
direcs =  [(1,0), (2,1), (1,1), (0,1), (1,-1), (1,2)]
direcs =  [(1,0), (2,1), (1,1), (0,1), (1,-1), (1,2), ]
direcs =  [(1,0), (2,1), (1,1), (1,2), (0,1), (-1,2),(-1,1), (-2,1)]
direcs = [(1,0),(0,1)] + [(np.random.normal(), np.random.normal()) for i in range(4)]
scale_factor = 20

width = 500
height = 500
d = draw.Drawing(width, height, origin='top-left')

d.append(draw.Lines(width*0.01, height*0.01,
                     width*0.01, height*0.99,
                     width*0.99, height*0.99,
                    width*0.99, height*0.01,
                    close=True,
            fill="#ffffff",#fill='#eeee00',
            stroke='black'))


def sum_vecs(v1,v2):
    return tuple( x1+x2 for x1,x2 in zip(v1,v2) )

test_sum = sum_vecs((3,4),(5,6))
print(f"Sum vecs (3,4)+(5,6) = {test_sum}")
red = set( [ zero_vec ] )
blue = set( [ direcs[0] ] )



print(f"red is {red}")
print(f"blue is {blue}")


for direc in direcs[1:]:
    print(f"Direc is {direc}")
    new_red = set([ sum_vecs(v,direc) for v in blue ])
    new_blue = set([ sum_vecs(v,direc) for v in red ])
    red_with_duplicates = red | new_red
    blue_with_duplicates = blue | new_blue
    # remove duplicates
    red = red_with_duplicates - blue_with_duplicates
    blue = blue_with_duplicates - red_with_duplicates
    print(f"\nAdding direc {direc}:")
    print(f"red ={red}")
    print(f"blue={blue}")

all_x = [v[0] for v in red | blue]
all_y = [v[1] for v in red | blue]
x_min = min( all_x )
x_max = max( all_x )
y_min = min( all_y )
y_max = max( all_y )
x_range = max(x_max-x_min, 1)
y_range = max(y_max-y_min, 1)
print(f"x range {x_min} to {x_max} and y range {y_min} to {y_max}")

def my_colour(n):
    cols = ["black", "red", "blue","green","magenta","pink","orange"]
    if n<0 or n>=len(cols):
        n=0
    return cols[n]
for v in red:
    for n,direc in enumerate(direcs):
        sf = len(direcs)
        x1 = (v[0]-sf*direc[0]-x_min)/x_range # in [0,1]
        y1 = (v[1]-sf*direc[1]-y_min)/y_range # in [0,1]
        x2 = (v[0]+sf*direc[0]-x_min)/x_range # in [0,1]
        y2 = (v[1]+sf*direc[1]-y_min)/y_range # in [0,1]

        x1 = width * (0.05 * (1 - x1) + 0.95 * x1)  # in [0, width]
        y1 = height * (0.05 * (1 - y1) + 0.95 * y1)  # in [0, width]
        x2 = width * (0.05 * (1 - x2) + 0.95 * x2)  # in [0, width]
        y2 = height * (0.05 * (1 - y2) + 0.95 * y2)  # in [0, width]

        d.append(draw.Lines(x1,y1, x2,y2,
                            stroke=my_colour(n),
                            #stroke='black',
                            ))


for colour, vertices in ( ('red',red), ('blue',blue)):
    for v in vertices:
        x = (v[0]-x_min)/x_range # in [0,1]
        y = (v[1]-y_min)/y_range # in [0,1]

        x = width * (0.05 * (1 - x) + 0.95 * x)  # in [0, width]
        y = height * (0.05 * (1 - y) + 0.95 * y)  # in [0, width]

        r = min(width, height)/2/40
        #print(f"Drawing a radius {r} {colour} circle at ({x}, {y}) ")
        d.append(draw.Circle(x, y, r, fill=colour,
                             #stroke_width=1,
                             #stroke='black'
                             ))

    """
    d.append(draw.Lines(0, 45,
                     70, 49,
                     95, -49,
                    -90, -40,
                    close=True,
            fill='#eeee00',
            stroke='black'))
    """



d.save_svg('example.svg')
print("In ")
print(os.getcwd())
print("created example.svg")