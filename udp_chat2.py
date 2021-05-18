import socket
import threading
import PySimpleGUI as sg

SERVER_HOST = "192.168.137.1"
PORT = 8080
CLIENT_HOST = "192.168.137.59"

CODE = "UTF-8"


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    layout = [[sg.Multiline("", size=(90, 20), k="content", disabled=True, autoscroll=True),
               sg.Multiline("", size=(10, 10), k="tip", disabled=True)],
              [sg.Multiline("", size=(45, 5), k="-in-")],
              [sg.B("发送"), sg.B("退出"), sg.B("skip")]]
    window = sg.Window('client', layout, return_keyboard_events=True)

    t1 = threading.Thread(target=recv, args=(udp_socket, window))
    t1.start()
    global content
    content = ""
    while True:
        event, value = window.read()
        if event == '发送' or event == '\r':
            udp_socket.sendto(value["-in-"].replace('\n', '').replace('\r', '').encode(CODE), (CLIENT_HOST, PORT))
            window['tip'].update("已发送,等待回复")
            content += "【发送】" + value['-in-'].replace('\n', '').replace('\r', '') + "\n"
            window['content'].update(content)
            window['-in-'].update("")
            print("【发送】：" + value["-in-"].replace('\n', '').replace('\r', ''))
        if event == '退出' or event == sg.WINDOW_CLOSED:
            udp_socket.sendto("exit".encode(CODE), (SERVER_HOST, PORT))
            exit()


def recv(udp_socket, window):
    global content
    lock = threading.Lock()
    udp_socket.bind((SERVER_HOST, PORT))
    while True:
        msg = udp_socket.recv(1000).decode(CODE)
        if msg == "exit":
            exit()
        content += ("【接收】：" + msg + "\n")
        print("【接收】：" + msg)
        lock.acquire()
        window['tip'].update('已接收信息')
        window['content'].update(content)
        lock.release()


if __name__ == "__main__":
    main()
