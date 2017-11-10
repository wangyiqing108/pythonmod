import select
import socket

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(("127.0.0.1", 8889))
listen_sock.listen(10)
listen_sock.setblocking(0)
epoll_sock = select.epoll()
epoll_sock.register(listen_sock.fileno(), select.EPOLLIN )

fdsock = {
    listen_sock.fileno(): listen_sock,
}
print listen_sock.fileno(),listen_sock
send = 0
buf = ""


while True:
    epoll_list = epoll_sock.poll()
    for fd, events in epoll_list:
       print fd,events
       if select.EPOLLIN & events:
           if fd == listen_sock.fileno():
               conn,addr = listen_sock.accept()
               conn.setblocking(0)
               print conn , addr ,conn.fileno()
               epoll_sock.register(conn.fileno(), select.EPOLLIN )
               fdsock[conn.fileno()] = conn
               print "fdsock-->",fdsock ,events
           else:
               print 'aa',fd
               buf += fdsock[fd].recv(1)
               print 'buf',buf
               if len(buf)>2 and buf[-2] == '\r' and buf[-1] == '\n':
                   buf = buf[:-2][::-1] + "\r\n"
                   #print buf
                   epoll_sock.unregister(conn)
                   epoll_sock.register(conn.fileno(), select.EPOLLOUT)
       elif select.EPOLLOUT & events:
           print send ,buf
           s = fdsock[fd].send(buf[send:])
           print 's',s
           if s > 0:
              send += s
           if send == len(buf):
               epoll_sock.unregister(conn)
               epoll_sock.register(conn.fileno(), select.EPOLLIN)
               send = 0
               buf = ""
