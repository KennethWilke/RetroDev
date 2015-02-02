from .lexer import lexer
from .parser import parser
from .common import instruction_set, opcodes, directives
from .targets import targets
import struct
import sys


def parse_source_file(source_file, process_state=None):
    ''' Parse dat source file! '''
    # Start process state if it doesn't already exist
    if process_state is None:
        process_state = {'cur_addr': 0,
                         'instructions': [],
                         'included_files': [source_file],
                         'identifiers': {},
                         'unresolved_identifiers': {}}
    else:
        process_state['included_files'].append(source_file)
    # Read source file
    with open(source_file) as src_file:
        source_text = src_file.read()
    expressions = parser.parse(source_text, lexer=lexer)
    process_expressions(expressions, process_state)
    return process_state


def process_expressions(expressions, process_state):
    #print expressions
    for op, value in expressions:
        if op in directives:
            handle_directive(process_state, op, value)
        elif op == 'LABEL':
            # Handle label referencing
            if value in process_state['identifiers']:
                print 'ERROR: Label "{0}" defined multiple '\
                      'times'.format(expression[1])
                sys.exit(1)
            else:
                process_state['identifiers'][value] = process_state['cur_addr']
        elif op == 'ASSIGNMENT':
            identifier, assignment_value = value
            # Handle label referencing
            if identifier in process_state['identifiers']:
                print 'ERROR: Identifier "{0}" defined multiple '\
                      'times'.format(identifier)
                sys.exit(1)
            else:
                process_state['identifiers'][identifier] = assignment_value
        elif op in instruction_set:
            handle_instruction(process_state, op, value)
        else:
            print "{0} NOT YET IMPLEMENTED".format(expression)
            sys.exit(1)

    # Second pass to resolve unresolved identifiers
    identifiers = process_state['identifiers']
    unresolved_identifiers = process_state['unresolved_identifiers']
    for identifier in unresolved_identifiers:
        if identifier not in identifiers:
            print 'Identifier {0} used but not set'.format(identifier)
            sys.exit(1)
        val = struct.pack('<H', identifiers[identifier])
        ins_offset = int(unresolved_identifiers[identifier])
        instructions[ins_offset] = val[0]
        instructions[ins_offset + 1] = val[1]


def handle_directive(process_state, directive, value):
    if directive == 'ORG':
        # Set origin
        if type(value) == tuple:
            # If it's a tuple it's an identifier
            identifier = value[1]
            try:
                new_cur_addr = process_state['identifiers'][identifier]
            except KeyError:
                print 'Unset id {0} used for directive'.format(identifier)
                sys.exit(1)
            process_state['cur_addr'] = new_cur_addr
        else:
            process_state['cur_addr'] = value
    elif directive == 'TARGET':
        # See if target is handled
        value = value.lower()
        if value not in targets:
            print 'Unknown target: {0}'.format(value)
            sys.exit(1)
        # If it is, store it in the process state
        process_state['target'] = value
        process_state['write'] = targets[value]
    elif directive == 'INCLUDE':
        if value in process_state['included_files']:
            print "File already included: {0}".format(value)
            sys.exit(1)
        # Save unresolved identifiers
        unresolved_locally = process_state['unresolved_identifiers']
        process_state['unresolved_identifiers'] = {}
        # Parse included files
        parse_source_file(value, process_state)
        # Restore unresolved identifiers
        process_state['unresolved_identifiers'] = unresolved_locally
    else:
        print 'Unhandled directive: {0}'.format(directive)
        sys.exit(1)


def handle_instruction(process_state, op, value):
    # Implied operations take no arguments
    if not len(value):
        try:
            opcode = opcodes[op]['IMPLIED']
        except KeyError:
            print '{0} has no implied call type defined'.format(op)
            sys.exit(1)
        process_state['instructions'].append(struct.pack('B', opcode))
        process_state['cur_addr'] += 1
        return

    # Get call type and value
    call_type, value = value
    # Get opcode value
    try:
        # Branch instructions only have ZERO, but the parser returns ABSOLUTE
        if op.startswith('B'):
            opcode = opcodes[op]['ZERO']
        else:
            opcode = opcodes[op][call_type]
    except KeyError:
        print '{0} has no {1} call type defined'.format(op, call_type.lower())
        sys.exit(1)

    # Push value into instructions based on call type
    if call_type == 'IMMEDIATE':
        process_state['instructions'].append(struct.pack('B', opcode))
        # If string, pack first byte. Otherwise pack numberic value
        if type(value) == str:
            process_state['instructions'].append(struct.pack('c', value[0]))
        elif value < 0:
            process_state['instructions'].append(struct.pack('b', value))
        else:
            process_state['instructions'].append(struct.pack('B', value))
        # Immediate calls are 2 bytes long
        process_state['cur_addr'] += 2
    elif call_type == 'ABSOLUTE':
        if type(value) == tuple and\
          value[0] == 'IDENTIFIER':
            process_state['instructions'].append(struct.pack('B', opcode))
            identifier = value[1]
            try:
                value = int(process_state['identifiers'][identifier])
                if value < 0:
                    packed_value = struct.pack('<h', value)
                else:
                    packed_value = struct.pack('<H', value)
            except KeyError:
                packed_value = ['\x00', '\x00']
                id_offset = len(process_state['instructions'])
                process_state['unresolved_identifiers'][identifier] = id_offset
            process_state['instructions'].append(packed_value[0])
            process_state['instructions'].append(packed_value[1])
            process_state['cur_addr'] += 3
        elif value > 255 or value < -127:
            process_state['instructions'].append(struct.pack('B', opcode))
            if value < 0:
                val = struct.pack('<h', value)
            else:
                val = struct.pack('<H', value)
            process_state['instructions'].append(val[0])
            process_state['instructions'].append(val[1])
            process_state['cur_addr'] += 3
        else:
            opcode = opcodes[op]['ZERO']
            process_state['instructions'].append(struct.pack('B', opcode))
            if value < 0:
                process_state['instructions'].append(struct.pack('b', value))
            else:
                process_state['instructions'].append(struct.pack('B', value))
            process_state['cur_addr'] += 2
    elif expression[1][0] == 'OFFSET':
        if expression[1][2] > 255:
            opcode = opcodes[expression[0]][expression[1][0]][expression[1][1]]['ABSOLUTE']
            instructions.append(struct.pack('B', opcode))
            val = struct.pack('<H', expression[1][2])
            instructions.append(val[0])
            instructions.append(val[1])
            cur_addr += 3
        else:
            opcode = opcodes[expression[0]][expression[1][0]][expression[1][1]]['ZERO']
            instructions.append(struct.pack('B', opcode))
            val = expression[1][2]
            instructions.append(struct.pack('B', val))
            cur_addr += 2
    elif expression[1][0] == 'INDIRECT':
        if expression[0] == 'JMP':
            opcode = opcodes['JMP']['INDIRECT']
            instructions.append(struct.pack('B', opcode))
            val = struct.pack('<H', expression[1][1])
            instructions.append(val[0])
            instructions.append(val[1])
            cur_addr += 3
        else:
            opcode = opcodes[expression[0]][expression[1][0]][expression[1][1]]
            instructions.append(struct.pack('B', opcode))
            val = expression[1][2]
            instructions.append(struct.pack('B', val))
            cur_addr += 2
    elif expression[1][0] == 'REGISTER':
        opcode = opcodes[expression[0]][expression[1][0]][expression[1][1]]
        instructions.append(struct.pack('B', opcode))
        cur_addr += 1
    else:
        print expression
        print 'UNHANDLED INSTRUCTION ARGUMENT TYPE'
