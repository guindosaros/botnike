from dearpygui.core import *
from dearpyui.simple import *

# set_main_window_size(540,720)
# set_global_font_scale(1.25)
# set_theme('gold')


# with window('SNKRS BOOT APPLICATION', width=520,height=677):
#     print('Guiii Rounning')
#     set_window_pos("SNKRS BOOT)
#     add_drawing('logo', width=520,heigth=290)
#     add_separator()
#     add_spacing(count=12)
#     add_text("test de l'element",color=[232,163,33])
    
# draw_image('logo','nskr',[0,240])


def save_callback(sender, data):
    print("Save Clicked")
    
add_text("Hello, world")
add_button("Save", callback=save_callback)
add_input_text("string", default_value="Quick brown fox")
add_slider_float("float", default_value=0.273, max_value=1)


# 0767246833