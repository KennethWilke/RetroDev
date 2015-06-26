import struct


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
        outfile.write('\x4e\x45\x53\x1a')
        prg_count = (len(process_state['instructions']) / 16384) + 1
        outfile.write(struct.pack('B', prg_count))
        if 'nes_chrfiles' in process_state:
            outfile.write(struct.pack('B', len(process_state['nes_chrfiles'])))
        else:
            outfile.write('\x00')
        outfile.write('\x00\x00'
                      '\x00\x00\x00\x00'
                      '\x00\x00\x00\x00')
        size = 16
        for byte in process_state['instructions']:
            outfile.write(byte)
            size += 1
        while size < (prg_count * 16384) + 10:
            outfile.write('\x00')
            size += 1

        if 'nes_nmi' in process_state:
            if type(process_state['nes_nmi']) == tuple:
                nmi = process_state['identifiers'][process_state['nes_nmi'][1]]
            else:
                nmi = process_state['nes_nmi']
        else:
            nmi = 0xC000
        outfile.write(struct.pack('<H', nmi))

        if 'nes_reset' in process_state:
            if type(process_state['nes_reset']) == tuple:
                ident = process_state['nes_reset'][1]
                reset = process_state['identifiers'][ident]
            else:
                reset = process_state['nes_reset']
        else:
            reset = 0xC000
        outfile.write(struct.pack('<H', reset))
        
        if 'nes_irq' in process_state:
            if type(process_state['nes_irq']) == tuple:
                irq = process_state['identifiers'][process_state['nes_irq'][1]]
            else:
                irq = process_state['nes_irq']
        else:
            irq = 0xC000
        outfile.write(struct.pack('<H', irq))
        
        if 'nes_chrfiles' in process_state:
            for chrfile in process_state['nes_chrfiles']:
                chrfile_size = 0
                with open(chrfile) as chrfilep:
                    chrdata = chrfilep.read()
                    chrfile_size = len(chrdata)
                    outfile.write(chrdata)
                while chrfile_size < 8192:
                    outfile.write('\x00')
                    chrfile_size = chrfile_size + 1


def write_2600(process_state, outfile_name):
    with open(outfile_name, 'w') as outfile:
        size = 0
        for byte in process_state['instructions']:
            outfile.write(byte)
            size += 1
        while size < 4090:
            outfile.write('\xFF')
            size += 1

        for vector in ['atari_nmi', 'atari_reset', 'atari_irq']:
            if vector in process_state:
                if type(process_state[vector]) == tuple:
                    ident = process_state[vector][1]
                    addr = process_state['identifiers'][ident]
                else:
                    addr = process_state[vector]
            else:
                addr = 0xF000
            outfile.write(struct.pack('<H', addr))


targets = {'appleii': write_appleii_dsk,
           'nes': write_ines,
           'atari_2600': write_2600}
