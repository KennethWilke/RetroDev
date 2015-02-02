def write_appleii_dsk(process_state, outfile_name):
    with open(outfile_name, 'w') as outfile:
        outfile.write('\x01')
        size = 1
        for byte in process_state['instructions']:
            outfile.write(byte)
            size += 1
        while size < 143360:
            outfile.write('\xFF')
            size += 1


def write_ines(process_state, outfile_name):
    with open(outfile_name, 'w') as outfile:
        outfile.write('NES\x1a\x01\x00\x00\x00'
                      '\x00\x00\x00\x00\x00\x00\x00\x00')
        size = 16
        for byte in process_state['instructions']:
            outfile.write(byte)
            size += 1
        while size < 0x400A:
            outfile.write('\x00')
            size += 1
        outfile.write('\x00\xC0\x00\xC0\x00\x00')


targets = {'appleii': write_appleii_dsk,
           'nes': write_ines}
