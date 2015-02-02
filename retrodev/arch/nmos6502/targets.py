def write_appleii_dsk(process_state, outfile_name):
    with open(outfile_name, 'w') as outfile:
        outfile.write('\x01')
        size = 1
        for byte in process_state['instructions']:
            outfile.write(byte)
            size += 1
        while size < 143360:
            outfile.write('\x00')
            size += 1

targets = {'appleii': write_appleii_dsk}
