from subprocess import Popen
from time import strftime
import tkinter.ttk
from tkinter.messagebox import showerror
import traceback

from serial.tools.list_ports import comports

from . import usb_ids


def main():
    ports = comports()

    top = tkinter.Tk()
    top.title('COM Ports')

    ports_listbox = tkinter.Listbox(top, width=150, height=15, exportselection=False)
    ports_listbox.pack(fill=tkinter.BOTH, expand=1)

    for i in ports:
        ports_listbox.insert(tkinter.END, '{}: {} [{} {}]'.format(i.device, i.description, *usb_ids.get(i.vid or 0, i.pid or 0)))

    ports_listbox.select_set(0, 0)

    baud_rate_combobox = tkinter.ttk.Combobox(top)
    baud_rate_combobox.pack(side=tkinter.LEFT)

    baud_rate_combobox['values'] = list(map(str, (110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000)))
    baud_rate_combobox.set('115200')

    ports_listbox.focus()

    def ok(_event=None):
        try:
            sel = ports_listbox.curselection()
            print(sel)
            if sel:
                port = ports[sel[0]].device
                baud_rate = baud_rate_combobox.get()
                time_str = strftime('%Y%m%d_%H%M%S')
                logfile = r'C:\Temp\putty_{}_{}_{}.log'.format(time_str, port, baud_rate)
                cmd = ['putty', '-serial', port, '-sercfg', baud_rate + ',8,n,1,N', '-sessionlog', logfile]

                print(' '.join(cmd))
                Popen(cmd)
        except Exception:
            showerror('Error opening PuTTY!', traceback.format_exc())

        top.destroy()

    def cancel(_event=None):
        top.destroy()

    ports_listbox.bind('<Double-1>', ok)
    top.bind('<Return>', ok)
    top.bind('<Escape>', cancel)

    top.focus_force()
    top.mainloop()


if __name__ == '__main__':
    main()
