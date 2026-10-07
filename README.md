this basically makes it easier to make games for my friends, to the extent that it allows one to make games in a few lines. work in progress lol. there are two layers of abstraction and then a framework.\\

# layer  1:\

layer 1 has two subparts:
- netcode abstraction
- pygame abstraction\

## netcode abstraction:\

this was the original purpose of awooga\
it makes network stuff for videogames easier, such that you dont have to fuck around with raw sockets and shit\\

so sendData() first sends the length of the message wrapped in four bytes, then it sends the actual message.\
it takes the following args: conn (the connection object), and datum (the datum/message to be sent), and returns nothing\\

recvData() listens for four bytes for the message length, then listens for whatever message length was sent using recvExact().\
it takes the following args: conn (the connection object). it returns the message.\\

decoding and encoding are handled by sendData() and recvData(), and they are intended to be able to send and receive the following data types:\
- str
- byte or bytearray
- int
- lists or dicts or that sort of thing\

now if you dont want to deal with sendData() and recvData(), you can use sendRecv().\
sendRecv() takes the following args: data, and choice, whose default value is "s-c"\
if the program is initialized like this:\
```batch
python program.py host 5000
```
it will host the game, and once `__init__()` is ran on the client using `n = net.main()`, the client will connect to the server, and so if you run:
```python
n.sendRecv(data=data, choice="s-c")
```
on the server, it will send the data to the client, but conversely, if you run
```python
data = n.sendRecv(choice="c-s")
```
it will receive the data and store it in data.\\

this makes it easier to send and receive data, so instead of having to deal with long and boring sockets programming just to send hello world, you can do:
```python
import net

n = net.main()
r = n.sendRecv(data="Hello, World!", choice="c-s")
print(r)
r = n.sendRecv(data="Hello, World!", choice="s-c")
print(r)
```
