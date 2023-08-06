"""The PipeSerial testsuite."""
from pipeserial import pipeserial


def test_pipeserial() -> None:
    """Testing basic functionality."""
    sp = pipeserial.PipeSerial(serialport="/dev/something")
    assert sp.ser.port == "/dev/something"
