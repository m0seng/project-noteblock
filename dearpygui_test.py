import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=600)

with dpg.window() as window:
    dpg.add_button(label="yay")
    dpg.add_button(label="bruh", height=-30)
    dpg.add_button(label="stuff", height=25)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()