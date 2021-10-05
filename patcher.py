#!/bin/env python3
from sys import argv
# Processor architecture byte-value pair for the ELF file format
machines = {b"\x3e\x00":"x86_64", b"\x28\x00":"armv7", b"\xb7\x00":"armv8"}

argc = len(argv)
if (argc > 3):
    print("Usage: ", argv[0], "[<input_file> [<output_file>]]\n\n<input_file> defaults to \"libflutter.so\"\n<output_file> defaults to \"patched.so\"")
    exit(-1)

infile = "libflutter.so"
outfile = "patched.so"
if (argc > 1):
    infile = argv[1]
if (argc > 2):
    outfile = argv[2]

print("Opening", infile)
fp = open(infile, "rb")
libflutter = bytearray(fp.read())
fp.close()

e_machine = bytes(libflutter[0x12:0x14]) # 0x12 is the e_machine offset for the ELF
try:
    arch = machines[e_machine]
except:
    arch = "Unkown"
    print("Unknow architecture or invalid ELF! (e_machine = 0x"+ e_machine.hex()+")")
    exit(-1)

print("Architecture", arch, "identified")

print("Reading signatures at", "./signatures/"+arch)
fp = open("./signatures/"+arch, "rt")
signatures_hex = fp.read().split("\n")[:-1]
fp.close()

signatures = []
for signature_hex in signatures_hex:
    print("Loading signature:", signature_hex)
    signatures.append(bytes.fromhex(signature_hex))


print("Searching for signatures in", infile)
signature_count = 0
patch_offset = -1
for signature in signatures:
    offset = -1
    nxt = 0
    while(nxt != -1):
        nxt = libflutter.find(signature, offset+1)
        if (nxt != -1):
            offset = nxt
            signature_count += 1
            print("Assinatura", signature.hex(), "em", hex(offset))
            if patch_offset == -1:
                patch_offset = offset

if (signature_count == 0):
    print("No signature found at", infile)
    exit(-1)
elif(signature_count > 1):
    print("Multiple signatures found,", signature_count)
    exit(-1)

# Apenas uma assinatura, aplicar patch
print("Reading patch from", "./patches/"+arch)
fp = open("./patches/"+arch, "rt")
patch_hex = fp.read().split("\n")[0]
print("Loading patch", patch_hex)
patch = bytes.fromhex(patch_hex)
fp.close()

# Modifica os bytes do arquivo
print("Applying patch at offset", hex(patch_offset))
for i, b in enumerate(patch):
    libflutter[patch_offset+i] = b

# Salva o arquivo
print("Saving patched lib at", outfile)
fp = open(outfile, "wb")
fp.write(libflutter)
fp.close()

exit(0)
