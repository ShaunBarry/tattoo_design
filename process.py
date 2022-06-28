import drawSvg as draw
import numpy as np

axis_length = 85
SIZE = 250
axis_label_font_size = 16
theta = np.pi/3.0
R_circle = 80
R_angle = 10
marker_len = 8

circle_thickness = 2.0
trig_thickness = 1.0
axes_thickness = 1.0
vec_thickness = 1.2
annotate_thickness = 0.3

dashed_line_pattern = "5 5"

right_angle_size = 7.25
dx = 2
dy = 2
annotate_height = 2

use_axis_arrows = False
use_in_components = True
use_right_angle = True
use_annotations = True

x_coord1 = (R_circle-marker_len)*np.cos(theta)
y_coord1 = (R_circle-marker_len)*np.sin(theta)
x_coord2 = R_circle*np.cos(theta)
y_coord2 = R_circle*np.sin(theta)

d = draw.Drawing(SIZE, SIZE, origin='center', displayInline=False)

d.append(draw.Rectangle(-SIZE//2,-SIZE//2,SIZE,SIZE, fill='white'))


# Draw a circle
d.append(draw.Circle(0, 0, R_circle,
            fill='none', stroke_width=circle_thickness, stroke='black'))

# Draw text
#d.append(draw.Text('$/textbf{Basic}$', 8, -10, 35, fill='red'))  # Text with font size 8
#d.append(draw.Text('Path text', 8, path=p, text_anchor='start', valign='middle'))
#d.append(draw.Text(['Multi-line', 'text'], 8, path=p, text_anchor='end'))
#d.append(draw.Text('$1$', axis_label_font_size, 85, -3, fill='black'))
#d.append(draw.Text('$-1$', axis_label_font_size, -102, -3, fill='black'))
#d.append(draw.Text('$j$', axis_label_font_size, 0, 90, fill='black'))
#d.append(draw.Text('$-j$', axis_label_font_size, 0, -90, fill='black'))

### define arrow_head ###
arrow_head = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=marker_len, orient='auto')
arrow_head.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))

if use_axis_arrows:
    m_head = arrow_head
else:
    m_head = 'none'

### draw axes lines ###
p = draw.Path(stroke='black', stroke_width=axes_thickness, fill='none', marker_end=m_head) 
p.M(0, -axis_length).L(0, axis_length)
d.append(p)

p = draw.Path(stroke='black', stroke_width=axes_thickness, fill='none', marker_end=m_head)  # Add an arrow to the end of a path
p.M(-axis_length, 0).L(axis_length, 0)
d.append(p)


### draw vector arrow line ###
p = draw.Path(stroke='black', stroke_width=vec_thickness, fill='none', marker_end=arrow_head)
p.M(0, 0).L(x_coord1, y_coord1)
d.append(p)

### draw trig lines ###
if use_in_components:
    p = draw.Path(stroke='black', stroke_width=trig_thickness, fill='none', stroke_dasharray=dashed_line_pattern)
    p.M(x_coord2, 0).L(x_coord2, y_coord2)
    d.append(p)

    p = draw.Path(stroke='black', stroke_width=trig_thickness, fill='none', stroke_dasharray=dashed_line_pattern) 
    p.M(0, y_coord2).L(x_coord2, y_coord2)
    d.append(p)

### angle ###
p = draw.Arc(0, 0, R_angle, 0, theta*(180/np.pi), stroke='black', stroke_width=trig_thickness, fill='none', cw=False)#, **kwargs)
#p.M(R_angle, 0).L(R_angle*np.cos(theta), R_angle*np.sin(theta))
d.append(p)


### right angle ###
if use_right_angle:
    p = draw.Rectangle(x=(x_coord2-right_angle_size), y=0,
                    width=right_angle_size, height=right_angle_size,
                    stroke='black', stroke_width=trig_thickness, fill='none')
    d.append(p)

if use_annotations:
    ### y annotate ###
    p = draw.Path(stroke='black', stroke_width=annotate_thickness, fill='none')
    p.M(-dx, y_coord2).L(-dx-annotate_height, y_coord2).L(-dx-annotate_height, 0)
    d.append(p)

    ### x annotate ###
    p = draw.Path(stroke='black', stroke_width=annotate_thickness, fill='none')
    p.M(x_coord2, -dy).L(x_coord2, -dy-annotate_height).L(0, -dy-annotate_height)
    d.append(p)

#d.setPixelScale(100)  # Set number of pixels per geometry unit
d.setRenderSize(1600,1600)  # Alternative to setPixelScale

### export ###
d.saveSvg('figures/example.svg')
d.savePng('figures/example.png')