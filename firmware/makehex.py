from sys import argv

binfile = argv[1]
nparts  = int(argv[2])
nwords  = int(argv[3])
output_ext = argv[4]

assert binfile[-4:] == ".bin", "Bin file not ending with .bin"
firmware_name = binfile[:-4]

with open(binfile, "rb") as f:
    bindata = f.read()

if (len(bindata) > 4*(nwords*nparts)):
    raise Exception("Program longer than allowed size")

full_hex = []
for i in range(nwords*nparts):
    if i < len(bindata) // 4:
        w = bindata[4*i : 4*i+4]
        full_hex.append("%02x%02x%02x%02x" % (w[3], w[2], w[1], w[0]))
    else:
        full_hex.append("00000000")

if (nparts == 1):
    fout = open(firmware_name + "_%s.hex"%output_ext, "w")
    for k in range(nwords):
        fout.write(full_hex[k] + "\n")
    fout.close()
else:
    for n in range(nparts):
        fout = open(firmware_name + "_%s%d.hex"%(output_ext, n), "w")
        for k in range(nwords):
            fout.write(full_hex[nwords*n+k] + "\n")
        fout.close()
