import sounddevice as sd
import tkinter as tk
import tkinter.ttk as ttk

class DeviceSelect(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.device_name = tk.StringVar()
        self.combo_device = ttk.Combobox(self, textvariable=self.device_name, width=50)
        self.combo_device["values"] = self.get_device_names()
        self.combo_device.grid(padx=5, pady=5)

        self.btn_set_device = ttk.Button(self, text="Set device", command=self.set_device)
        self.btn_set_device.grid(padx=5, pady=5)

    def get_device_names(self):
        devices = sd.query_devices()
        return [device["name"] for device in devices]

    def set_device(self, *args):
        device = self.device_name.get()
        stream = sd.OutputStream(device=device)

def main():
    root = tk.Tk()
    device_select = DeviceSelect(root)
    device_select.grid(padx=5, pady=5)
    root.mainloop()

if __name__ == "__main__":
    main()