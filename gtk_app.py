import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib, Gio

# Add a CSS provider
css_provider = Gtk.CssProvider()
css_provider.load_from_path('style.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default parameters for the window
        self.set_default_size(600, 250)
        self.set_title("MyApp")


        # Create an Header bar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # Add an Open Button to the HeaderBar
        self.open_button = Gtk.Button(label="Open")
        self.open_button.set_icon_name("document-open-symbolic")
        self.header.pack_start(self.open_button)

        # Create a file chooser dialog
        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")

        # Connect the open button to the file dialog
        self.open_button.connect('clicked', self.show_open_dialog)

        # Create a filter
        f = Gtk.FileFilter()
        # f.set_name("Image files")
        f.add_mime_type("image/jpeg")
        f.add_mime_type("image/png")

        filters = Gio.ListStore.new(Gtk.FileFilter)  # Create a ListStore with the type Gtk.FileFilter
        filters.append(f)  # Add the file filter to the ListStore. You could add more.

        self.open_dialog.set_filters(filters)  # Set the filters for the open dialog
        self.open_dialog.set_default_filter(f)

        # Create 3 boxes
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Create a button and define what to do when clicked
        self.button = Gtk.Button(label="Hello")
        self.button.connect('clicked', self.hello)

        # Adding the box1 to the window
        self.set_child(self.box1)  # Horizontal box to window

        # Append boxes 2 and 3 to box 1 (which are vertically aligned inside box 1 which is horizontal)
        self.box1.append(self.box2)  # Put vert box in that box
        self.box1.append(self.box3)  # And another one, empty for now

        # Add button to box2
        self.box2.append(self.button) # Put button in the first of the two vertial boxes

        # Create a CheckButton
        self.check_button = Gtk.CheckButton(label="Goodbye!")

        # Add a CheckButton to box3
        self.box2.append(self.check_button)

        # # Create group of check buttons, known as "radio buttons"
        # self.radio1 = Gtk.CheckButton(label="test")
        # self.radio2 = Gtk.CheckButton(label="test")
        # self.radio3 = Gtk.CheckButton(label="test")

        # # I don't understand this logic :(
        # self.radio1.set_group(self.radio2)
        # self.radio1.set_group(self.radio3)
        # self.radio1.connect("toggled", self.radio_toggled)

        # # Append radio buttons to box3
        # self.box3.append(self.radio1)
        # self.box3.append(self.radio2)
        # self.box3.append(self.radio3)

        # Create a switch box
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2.append(self.switch_box)

        # Create a switch and append it to the box
        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        self.switch.connect("state-set", self.switch_method)
        self.switch_box.append(self.switch)

        # Labelling the switch
        self.switch_label = Gtk.Label(label="This is a switch")
        self.switch_box.append(self.switch_label)
        self.switch_box.set_spacing(5)

        # Create a label and customize it using CSS
        self.label = Gtk.Label(label="This is some label")
        self.box3.append(self.label)
        self.label.set_css_classes(['title'])

        # Adding a slider
        self.slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.slider.set_digits(1)
        #self.slider.set_has_origin(True)
        self.slider.set_draw_value(True)
        self.slider.set_range(0, 10)
        self.slider.connect("value-changed", self.slider_method)
        self.box3.append(self.slider)

    # Add method hello, connecting to button and checkbutton
    def hello(self, button):
        print("Hello world")
        if self.check_button.get_active():
            print("Goodbye world!")
            self.close()

    # # Add radio_toggled method for radio buttons
    # def radio_toggled(self, button):
    #     if self.radio1.get_active() and self.radio2.get_active():
    #         print(":)")
    #     else:
    #         print(":(")

    # Add switch method
    def switch_method(self, switch, state):
        print(self.switch.get_state)
        if state:
            print("It's on!")

    # Add slider method
    def slider_method(self, slider):
        if slider.get_value() == 5:
            print("It is 5!!")

    def show_open_dialog(self, button):
        self.open_dialog.open(self, None, self.open_dialog_open_callback)

    def open_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                print(f"File path is {file.get_path()}")
                # Handle loading file from here
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")



class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
