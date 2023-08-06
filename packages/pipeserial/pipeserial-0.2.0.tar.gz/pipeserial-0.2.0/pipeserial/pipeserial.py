"""PipeSerial v0.2.0 module.

Source code available at https://github.com/tykling/pipeserial/
Can be installed from PyPi https://pypi.org/project/pipeserial/
Read more at https://pipeserial.readthedocs.io/en/latest/
"""

import argparse
import logging
import sys
import time
import typing

import serial  # type: ignore
from pexpect_serial import SerialSpawn  # type: ignore

__version__ = "0.2.0"
logger = logging.getLogger("pipeserial.%s" % __name__)


class PipeSerial:
    """The PipeSerial class."""

    __version__ = __version__

    def __init__(
        self,
        serialport: str,
        baudrate: int = 115200,
        bytesize: int = 8,
        parity: str = "N",
        stopbits: float = 1,
        rtscts: bool = False,
        xonxoff: bool = False,
        rts: typing.Optional[int] = None,
        dtr: typing.Optional[int] = None,
    ) -> None:
        """Initialise pyserial object and configure the serial port.

        Args:
            serialport: The serial port device to use, like "/dev/cuaU0"
            baudrate: The serial port speed, default: 115200
            bytesize: Serial port bytesize, one of {5 6 7 8}, default: 8
            parity: Serial port parity, one of {N E O S M}, default: N
            stopbits: Serial port stopbits, one of {1 1.5 2}, default: 1
            rtscts: Enable serial port RTS/CTS hardware flow control, default: False
            xonxoff: Enable serial port software flow control, default: False
            rts: Set initial RTS line state, one of {0, 1}, default: None
            dtr: Set initial DTR line state, one of {0, 1}, default: None

        Returns:
            Nothing
        """
        logger.debug(f"Configuring serial port {serialport} ...")
        self.ser = serial.serial_for_url(serialport, do_not_open=True)
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        self.ser.rtscts = rtscts
        self.ser.xonxoff = xonxoff
        if rts is not None:
            self.ser.rts = rts
        if dtr is not None:
            self.ser.dtr = dtr

    def open(self) -> bool:
        """Open the serial port and initialise the pexpect_serial object.

        Args: None
        Returns: None
        """
        # open serial port
        try:
            logger.debug("Opening serial port...")
            self.ser.open()
        except serial.SerialException:
            logger.exception(f"Could not open serial port {self.ser.name}")
            return False
        # and init pexpect_serial object
        self.ss = SerialSpawn(self.ser)
        logger.debug("Serial port opened OK!")
        return True

    def run(
        self,
        payload: str,
        expect: typing.List[str],
        delay: float = 0.9,
        expectcount: int = 1,
        timeout: int = 30,
    ) -> typing.List[str]:
        """Send the payload to serial device.

        Args:
            payload: The payload to send to the serial device.
            expect: A list of regex to expect as the end of output.

        Returns:
            The output from the serial device as list of string, one for each line.
        """
        # send the input to serial, line by line, with \r\n newlines
        for line in payload.split("\n"):
            if not line:
                # skip empty lines
                continue
            logger.debug(f"Sending payload line: {line}")
            self.ss.send(line.strip() + "\r\n")
            time.sleep(delay)

        # Wait for some matching output
        output = b""
        logger.debug(
            f"Collecting output, looking for one of these regular expressions: {expect}"
        )
        logger.debug(f"Will stop collecting after {expectcount} matches")
        for i in range(1, expectcount + 1):
            match = self.ss.expect(expect, timeout=timeout)
            logger.debug(
                f"Found match: '{expect[match].strip()}' (match number {i} of {expectcount})"
            )
            # we want all the output, before and including the expected string
            output += self.ss.before + self.ss.after

        # decode, strip and return the lines of output
        logger.debug(
            f"Done! Returning {len(output)} bytes of output from serial device"
        )
        return [line.strip() for line in output.decode("LATIN1").split("\n")]

    def close(self) -> None:
        """Close the serial port."""
        logger.debug("Closing serial port...")
        self.ss.ser.close()
        logger.debug("Serial port closed")


def get_parser() -> argparse.ArgumentParser:
    """Create and return the argparse object."""
    import argparse

    parser = argparse.ArgumentParser(
        description=f"PipeSerial version {__version__}. Sends input to a serial device, awaits (expects) some text, and returns the output. See the manpage or ReadTheDocs for more info."
    )

    parser.add_argument("serialport", help="Serial port device")

    parser.add_argument(
        "baudrate",
        type=int,
        nargs="?",
        help="Set baud rate, default: %(default)s",
        default=115200,
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",
        dest="expectcount",
        help="Collect output from the serial device until this many regex matches, default: %(default)s",
        default=1,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const="DEBUG",
        help="Debug mode. Equal to setting --log-level=DEBUG.",
        default=argparse.SUPPRESS,
    )

    parser.add_argument(
        "-e",
        "--expect",
        action="append",
        type=str,
        help="Regular expressions to expect as end of the output. Can be specified multiple times, default: ['\r\nOK\r\n', '\r\nERROR\r\n']",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        dest="loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level. One of DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaults to INFO.",
        default="INFO",
    )

    parser.add_argument(
        "-p",
        "--payload",
        type=str,
        help="The payload to send to the serial device, instead of getting it from standard input. Default None.",
        default=None,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        dest="loglevel",
        const="WARNING",
        help="Quiet mode. No output at all if no errors are encountered. Equal to setting --log-level=WARNING.",
        default=argparse.SUPPRESS,
    )

    parser.add_argument(
        "-s",
        "--send-delay",
        type=float,
        nargs="?",
        dest="senddelay",
        help="Delay in seconds between sending each line of payload to the serial device, default: %(default)s",
        default=0.9,
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        nargs="?",
        dest="timeout",
        help="Timeout in seconds before giving up waiting for the expected output, default: %(default)s",
        default=30,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s version {__version__}",
        help="Show PipeSerial version and exit.",
    )

    # serial port options
    group = parser.add_argument_group("Serial port options")

    group.add_argument(
        "--bytesize",
        choices=[5, 6, 7, 8],
        type=int,
        help="Set bytesize, one of {5 6 7 8}, default: 8",
        default=8,
    )

    group.add_argument(
        "--parity",
        choices=["N", "E", "O", "S", "M"],
        type=str,
        help="Set parity, one of {N E O S M}, default: N",
        default="N",
    )

    group.add_argument(
        "--stopbits",
        choices=[1, 1.5, 2],
        type=float,
        help="Set stopbits, one of {1 1.5 2}, default: 1",
        default=1,
    )

    group.add_argument(
        "--rtscts",
        action="store_true",
        help="Enable RTS/CTS hardware flow control, default: off",
        default=False,
    )

    group.add_argument(
        "--xonxoff",
        action="store_true",
        help="Enable software flow control, default: off",
        default=False,
    )

    group.add_argument(
        "--rts",
        type=int,
        help="Set initial RTS line state, one of {0, 1}, default: none",
        default=None,
    )

    group.add_argument(
        "--dtr",
        type=int,
        help="Set initial DTR line state, one of {0, 1}, default: none",
        default=None,
    )
    return parser


def main() -> None:
    """Get args, initialise the PipeSerial object, send the input to the serial device, and return the output.

    Args: None
    Returns: None
    """
    # get argparse object and parse args
    parser = get_parser()
    args = parser.parse_args()

    # define the log format used for stdout depending on the requested loglevel
    if args.loglevel == "DEBUG":
        console_logformat = "%(asctime)s pipeserial %(levelname)s pipeserial.%(funcName)s():%(lineno)i:  %(message)s"
    else:
        console_logformat = "%(asctime)s pipeserial %(levelname)s %(message)s"

    # configure the log format used for console
    logging.basicConfig(
        level=getattr(logging, str(args.loglevel)),
        format=console_logformat,
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )

    # show version and exit?
    if args.version:
        logger.info(f"PipeSerial version {__version__}")
        sys.exit(0)

    logger.debug("Initialising the PipeSerial class")
    sp = PipeSerial(
        serialport=args.serialport,
        baudrate=args.baudrate,
        bytesize=args.bytesize,
        parity=args.parity,
        stopbits=args.stopbits,
        rtscts=args.rtscts,
        xonxoff=args.xonxoff,
        rts=args.rts,
        dtr=args.dtr,
    )

    # get the payload from stdin or use args?
    if args.payload:
        payload = args.payload
    else:
        payload = sys.stdin.read()
    logger.debug(f"Payload is {len(payload)} bytes")

    if args.expect:
        expect = args.expect
    else:
        expect = ["\r\nOK\r\n", "\r\nERROR\r\n"]
    logger.debug(f"Output to expect: {expect}")

    # open the serial port
    if not sp.open():
        logger.error("Unable to open serial port, bailing out!")
        sys.exit(1)

    # all good, go!
    try:
        output = sp.run(
            payload=payload,
            expect=expect,
            delay=args.senddelay,
            expectcount=args.expectcount,
        )
    finally:
        # close the serial port
        sp.close()

    logger.debug(
        f"Got {len(output)} lines of output from serial device {args.serialport}:"
    )
    for line in output:
        print(line)


def init() -> None:
    """Call the main() function if being invoked as a script. This is here just as a testable way of calling main()."""
    if __name__ == "__main__":
        main()


# call init(), which then calls main() when needed
init()
