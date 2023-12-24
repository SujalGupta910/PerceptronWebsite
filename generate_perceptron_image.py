from PIL import Image,ImageDraw,ImageColor,ImageFont
from PIL.ImageColor import colormap
import random
import colorsys

font = ImageFont.truetype("arial.ttf",40)
circle_radius = 50

def drawImg(perceptron,image_path):
    vector_size = len(perceptron.input_vector)
    image_size = (800, circle_radius*2*vector_size + 25*(vector_size+1))
    img = Image.new("RGB",image_size,"white")
    draw = ImageDraw.Draw(img)

    base_color = random.choice(list(colormap.keys()))
    color_list = gen_colors(base_color)
    print(f"colors: {color_list}")

    flayer_xpos = circle_radius+25
    flayer_ypos = [(125*i+75) for i in range(vector_size)]

    slayer_xpos = flayer_xpos+200
    slayer_ypos = image_size[1]/2

    olayer_xpos = slayer_xpos+200
    olayer_ypos =  slayer_ypos

    for ypoint in flayer_ypos :
        draw.line([(flayer_xpos,ypoint),(slayer_xpos,slayer_ypos)],fill="black",width=3)

    draw.line([(slayer_xpos,slayer_ypos),(olayer_xpos,olayer_ypos)],fill="black",width=3)

    color = color_list[0]
    for i,ypoint in enumerate(flayer_ypos) :
        circle_box = xy_to_boundingbox(flayer_xpos,ypoint,circle_radius)
        fill_color = color
        text_fill = "black"
        if perceptron.input_vector[i]==0 :
            fill_color = "white" # 0
        if i==len(perceptron.input_vector)-1 :
            fill_color = "black"
            text_fill = "white"
        draw.ellipse(circle_box,fill=fill_color,outline="black",width=3)
        draw.text((flayer_xpos,ypoint), str(perceptron.weights[i]), font=font, fill=text_fill, anchor="mm")

    color = color_list[1]
    circle_box = xy_to_boundingbox(slayer_xpos,slayer_ypos,circle_radius)
    draw.ellipse(circle_box,fill=color,outline="black",width=3)
    draw.text((slayer_xpos,slayer_ypos), str(perceptron.dot_product), font=font, fill="black", anchor="mm")

    color = color_list[2]
    circle_box = xy_to_boundingbox(olayer_xpos,olayer_ypos,circle_radius)
    draw.ellipse(circle_box,fill=color,outline="black",width=3)
    draw.text((olayer_xpos,olayer_ypos), str(perceptron.predict()), font=font, fill="black", anchor="mm")

    img.save(image_path)
    print(f"Saved image {image_path}")

def xy_to_boundingbox(x,y,radius) :
    # converting xy coordinated os a circle to its bounding box
    return [(x-radius,y-radius),(x+radius,y+radius)]

def gen_colors(base,num_colors=3,similarity=0.3) :
    base_rgb = ImageColor.getrgb(base)
    base_hsv = colorsys.rgb_to_hsv(base_rgb[0]/255.0, base_rgb[1]/255.0, base_rgb[2]/255.0)

    colors = [base_rgb]
    for _ in range(num_colors-1) :
        h = base_hsv[0] + random.uniform(-similarity,similarity)
        s = base_hsv[1] + random.uniform(-similarity,similarity)
        v = base_hsv[2] + random.uniform(-similarity,similarity)

        h = max(0, min(1,h))
        s = max(0, min(1,s))
        v = max(0, min(1,v))

        rgb = colorsys.hsv_to_rgb(h,s,v)
        rgb = tuple(int(x*255) for x in rgb)
        colors.append(rgb)

    return colors
