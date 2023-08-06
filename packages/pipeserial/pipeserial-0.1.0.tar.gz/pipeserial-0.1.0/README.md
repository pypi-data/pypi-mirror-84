# PipeSerial
PipeSerial is a command-line utility to send some input from stdin to a serial device and return the output on stdout.

A quick example:

```
[tykling@container1 ~]$ echo -ne "AT\nATI" | sudo venv/bin/python pipeserial.py -c 2 -d /dev/ttyU0.3
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.main():311:  Initialising the PipeSerial class
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.__init__():54:  Configuring serial port {serialport} ...
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.main():329:  Payload is 6 bytes
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.main():335:  Output to expect: ['\r\nOK\r\n', '\r\nERROR\r\n']
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.open():75:  Opening serial port...
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.open():82:  Serial port opened OK!
2020-10-31 22:49:42 +0000 pipeserial DEBUG pipeperial.run():107:  Sending payload line: AT
2020-10-31 22:49:43 +0000 pipeserial DEBUG pipeperial.run():107:  Sending payload line: ATI
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.run():114:  Collecting output, looking for one of these regular expressions: ['\r\nOK\r\n', '\r\nERROR\r\n']
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.run():116:  Will stop collecting after 2 matches
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.run():120:  Found match: 'OK' (match number 1 of 2)
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.run():120:  Found match: 'OK' (match number 2 of 2)
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.run():127:  Done! Returning 64 bytes of output from serial device
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.close():133:  Closing serial port...
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.close():135:  Serial port closed
2020-10-31 22:49:44 +0000 pipeserial DEBUG pipeperial.main():355:  Got 9 lines of output from serial device /dev/ttyU0.3:
AT
OK
ATI
Quectel
EC25
Revision: EC25EFAR06A06M4G

OK

[tykling@container1 ~]$
```

Read more on ReadTheDocs at https://pipeserial.readthedocs.io/en/latest/
