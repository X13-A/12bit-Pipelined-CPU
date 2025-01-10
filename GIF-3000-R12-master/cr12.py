#!/usr/bin/env python3

import argparse, re, sys

# the per instruction formats: 0, 1, 2, 3, 4, or 5
FORMATS = {
    'nop': 0,
    'add': 1,
    'sub': 1,
    'mult': 1,
    'div': 1,
    'mod': 1,
    'and': 1,
    'or': 1,
    'xor': 1,
    'not': 2,
    'addi': 3,
    'subi': 3,
    'multi': 3,
    'divi': 3,
    'modi': 3,
    'shli': 3,
    'shri': 3,
    'ld': 3,
    'sd': 3,
    'jalr': 3,
    'jal': 4,
    'bz': 4,
    'bnz': 4,
}

# the per instruction opcodes
OPCODES = {
    'nop': (0, 0),
    'add': (0, 1),
    'sub': (0, 2),
    'mult': (0, 3),
    'div': (1, 0),
    'mod': (1, 1),
    'and': (1, 2),
    'or': (1, 3),
    'xor': (2, 0),
    'not': (2, 3),
    'addi': 3,
    'subi': 4,
    'multi': 5,
    'divi': 6,
    'modi': 7,
    'shli': 8,
    'shri': 9,
    'ld': 10,
    'sd': 11,
    'jalr': 12,
    'jal': 13,
    'bz': 14,
    'bnz': 15,
}

# the architecture register names
REGISTERS = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
}


def compile(source):
    """
    Compile an R12 source code

    :param source: the list of source code lines.
    :raises: nothing.

    :returns: the list of binary string instructions.
    """
    code = []

    # process all statements
    for i, line in enumerate(source, start=1):
        # strip any white space
        line = line.strip()

        if not line or line[0] == '#':
            # skip empty or comment lines
            continue

        # separate opcode from arguments
        op, *args = line.split(maxsplit=1)

        try:
            code.append(
                FORMAT_PARSERS[FORMATS[op]](op, args[0].split(',') if args else None, i)
            )

        except Exception as err:
            print(f"erreur ligne {i}: opcode invalide {op}", file=sys.stderr)

    return code


def parse_format0(op, args, line):
    """Parse the nop instruction format: 'nop'."""
    return '{:0>3x}'.format(0)


def parse_format1(op, args, line):
    """Parse the first instruction format: 'op rd, rs1, rs2'."""
    rd, rs1, rs2 = map(str.strip, map(str.upper, args))

    if not rd in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rd}", file=sys.stderr)

    if not rs1 in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rs1}", file=sys.stderr)

    if not rs2 in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rs2}", file=sys.stderr)

    # return binary instruction string
    binstr = (
        f'{OPCODES[op][0]:04b}'
        f'{REGISTERS[rd]:02b}'
        f'{REGISTERS[rs1]:02b}'
        f'{REGISTERS[rs2]:02b}'
        f'{OPCODES[op][1]:02b}'
    )

    return '{:0>3x}'.format(int(binstr, 2))


def parse_format2(op, args, line):
    """Parse the second instruction format: 'op rd, rs1'."""
    rd, rs1 = map(str.strip, map(str.upper, args))

    if not rd in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rd}", file=sys.stderr)

    if not rs1 in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rs1}", file=sys.stderr)

    # return binary instruction string
    binstr = (
        f'{OPCODES[op][0]:04b}'
        f'{REGISTERS[rd]:02b}'
        f'{REGISTERS[rs1]:02b}'
        f'0011'
    )
    return '{:0>3x}'.format(int(binstr, 2))


def parse_format3(op, args, line):
    """Parse the second instruction format: 'op rd, rs1, imm4'."""
    rd, rs1, imm4 = map(str.strip, map(str.upper, args))

    if not rd in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rd}", file=sys.stderr)

    if not rs1 in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rs1}", file=sys.stderr)

    try:
        value = int(imm4)
        if not 0 <= value <= 15:
            print(f"erreur ligne {line}: valeur invalide {value}", file=sys.stderr)

    except:
        value = 0
        print(f"erreur ligne {line}: valeur invalide {imm4}", file=sys.stderr)

    # return binary instruction string
    binstr = (
        f'{OPCODES[op]:04b}'
        f'{REGISTERS[rd]:02b}'
        f'{REGISTERS[rs1]:02b}'
        f'{value:04b}'
    )

    return '{:0>3x}'.format(int(binstr, 2))


def parse_format4(op, args, line):
    """Parse the third instruction format: 'op rs, imm6'."""
    rs, imm6 = map(str.strip, map(str.upper, args))

    if not rs in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rs}", file=sys.stderr)

    try:
        value = int(imm6)
        if not -32 <= value <= 31:
            print(f"erreur ligne {line}: valeur invalide {value}", file=sys.stderr)

    except:
        value = 0
        print(f"erreur ligne {line}: valeur invalide {imm6}", file=sys.stderr)

    # create binary string
    if value < 0:
        # corriger pour le complément à deux
        value += 64

    binstr = (
        f'{OPCODES[op]:04b}'
        f'{REGISTERS[rs]:02b}'
        f'{value:06b}'
    )

    return '{:0>3x}'.format(int(binstr, 2))


FORMAT_PARSERS = [
    parse_format0,
    parse_format1,
    parse_format2,
    parse_format3,
    parse_format4,
]


if __name__ == '__main__':
    # define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    args = parser.parse_args()

    # read source file
    with open(args.source, 'r') as file:
        source = file.readlines()

    # compile source
    code = compile(source)
    print('v2.0 raw')
    print('\n'.join(code))
