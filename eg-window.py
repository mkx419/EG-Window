#!/usr/bin/env python3
import gi, json, subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

def select_window(number):
    class SelectWindow(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self, title=select_list[number]["desc"])
            self.selected = []
            above_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            below_layout = Gtk.Box()
            below_layout.set_homogeneous(True)
            root_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            compile_button_layout = Gtk.Box()
            compile_button_layout.set_homogeneous(True)
            compile_image_layout = Gtk.Box()
            compile_image_layout.set_homogeneous(True)

            for i in select_list[number]["list"].keys():
                name = i
                path = select_list[number]["list"][i]
            
                if path is None:
                    image = Gtk.Label(label="No Image")
                else:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 200, 200)
                    image = Gtk.Image.new_from_pixbuf(pixbuf)

                button = Gtk.ToggleButton(label=name)
                button.connect("toggled", self.on_button_toggled, name)
                try:
                    if name in selected[number]: button.set_active(True)
                except: pass

                compile_image_layout.pack_start(image, True, True, 5)
                compile_button_layout.pack_start(button, True, True, 5)
            
            above_layout.pack_start(compile_image_layout, True, True, 5)
            above_layout.pack_start(compile_button_layout, True, True, 5)
        
            if not number == 0:
                back_button = Gtk.Button(label="前へ")
                back_button.connect("clicked", self.back)
                below_layout.pack_start(back_button, True, True, 5)

            if number == len(select_list) - 1:
                end_button = Gtk.Button(label="終了")
                end_button.connect("clicked", self.end)
                below_layout.pack_start(end_button, True, True, 5)
            else:
                next_button = Gtk.Button(label="次へ")
                next_button.connect("clicked", self.next)
                below_layout.pack_start(next_button, True, True, 5)
        
            root_layout.pack_start(above_layout, True, True, 5)
            root_layout.pack_start(below_layout, True, True, 5)

            self.add(root_layout)

            
        def on_button_toggled(self, button, name):
            if button.get_active():
                self.selected.append(name)
            else:
                self.selected.remove(name)
        
        def next(self, button):
            selected[number] = self.selected
            self.close()
            select_window(number + 1)
        
        def back(self, button):
            selected[number] = self.selected
            self.close()
            select_window(number - 1)
        
        def end(self, button):
            output = []
            selected[number] = self.selected
            self.close()

            for i in selected:
                output.append(" ".join(selected[i]))
            
            print(" ".join(output))
    
    win = SelectWindow()
    win.show_all()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    global select_list, selected
    selected = {}

    with open("./eg-window.json") as f:
        select_list = json.load(f)
    
    select_window(0)