from PIL import Image,ImageDraw
from random import shuffle

def drawImg(perceptron,image_path):
    vector_size = len(perceptron.input_vector)
    radius = 50
    image_size = (800, radius*2*vector_size + 25*(vector_size+1))
    img = Image.new("RGB",image_size,"white")
    draw = ImageDraw.Draw(img)

    color_list = ["blue","red","black","green"]
    
    flayer_xpos = 75
    flayer_ypos = [(125*i+75) for i in range(vector_size)]
    
    slayer_xpos = flayer_xpos+200
    slayer_ypos = image_size[1]/2

    olayer_xpos = slayer_xpos+200
    olayer_ypos =  slayer_ypos

    for ypoint in flayer_ypos :
        draw.line([(flayer_xpos,ypoint),(slayer_xpos,slayer_ypos)],fill="black",width=3)
    
    draw.line([(slayer_xpos,slayer_ypos),(olayer_xpos,olayer_ypos)],fill="black",width=3)

    shuffle(color_list)
    color = color_list[0]
    for ypoint in flayer_ypos :
        circle_box = xy_to_boundingbox(flayer_xpos,ypoint,radius)
        draw.ellipse(circle_box,fill=color,outline="black")
    
    shuffle(color_list)
    color = color_list[0]
    circle_box = xy_to_boundingbox(slayer_xpos,slayer_ypos,radius)
    draw.ellipse(circle_box,fill=color,outline="black")

    shuffle(color_list)
    color = color_list[0]
    circle_box = xy_to_boundingbox(olayer_xpos,olayer_ypos,radius)
    draw.ellipse(circle_box,fill=color,outline="black")

    img.save(image_path)
    print(f"Saved image {image_path}")

def xy_to_boundingbox(x,y,radius) :
    # converting xy coordinated os a circle to its bounding box
    return [(x-radius,y-radius),(x+radius,y+radius)]