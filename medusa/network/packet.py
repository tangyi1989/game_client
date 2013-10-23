import struct
import StringIO



def encode(cmd, packet):
    	string_io = StringIO.StringIO()

    	proto_buf = packet.SerializeToString()
    	string_io.write(struct.pack(">I",  0xffffffff))
    	string_io.write(struct.pack(">I",  cmd))
    	string_io.write(struct.pack(">I",  len(proto_buf)))
    	string_io.write(proto_buf)

    	string_io.seek(0)

    	return string_io.read()

def decode(packet):
	pass
