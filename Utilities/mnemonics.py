def match_mnemonic (code_inst):
    for monic in mnemonics:
        if code_inst[0] == monic['mnemonic']:
            return monic
    return None

class AddressingModes:
    INH = 'INH'
    IMM = 'IMM'
    DIR = 'DIR'
    EXT = 'EXT'

mnemonics = [
    {
        'mnemonic':'ORG'
    },
    {
        'mnemonic':'ABA',
        'INH':'18 06',
        'syze':2
    },
    {
        'mnemonic':'ABX',
        'INH':'1A B5',
        'syze':2
    },
    {
        'mnemonic':'ABY',
        'INH':'19 ED',
        'syze':2
    },
    {
        'mnemonic':'ADCA',
        'IMM':'89 ii',
        'DIR':'99 dd',
        'EXT':'B9 hh ll',
        'syze': 2,
        'syze_ext':3
    },
    {
        'mnemonic':'ADCB',
        'IMM':'C9 ii',
        'DIR':'D9 dd',
        'EXT':'F9 hh ll',
        'syze':2,
        'syze_ext':3
    },
    {
        'mnemonic':'ADDA',
        'IMM':'8B ii',
        'DIR':'9B dd',
        'EXT':'BB hh ll',
        'syze':2,
        'syze_ext':3
    },
    {
        'mnemonic':'ADDB',
        'IMM':'CB ii',
        'DIR':'DB dd',
        'EXT':'FB hh ll',
        'syze':2,
        'syze_ext':3
    },
    {
        'mnemonic':'ADDD',
        'IMM':'C3 jj kk',
        'DIR':'D3 dd',
        'EXT':'F3 hh ll',
        'syze':2,
        'syze_ext':3
    },
    {
        'mnemonic':'ANDA',
        'IMM':'84 ii',
        'DIR':'94 dd',
        'EXT':'B4 hh ll',
        'syze':2,
        'syze_ext':3
    },
    {
        'mnemonic':'ANDB',
        'IMM':'C4 ii',
        'DIR':'D4 dd',
        'EXT':'F4 hh ll',
        'syze':2,
        'syze_ext':3
    },
    {
        'mnemonic':'ANDCC',
        'IMM':'10 ii',
        'size':2
    },
    {
        'mnemonic':'ASL',
        'EXT':'78 hh ll',
        'size':3
    },
    {
        'mnemonic':'ASLA',
        'INH':'48',
        'size':1
    },
    {
        'mnemonic':'ASLB',
        'INH':'58',
        'size':1
    },
    {
        'mnemonic':'ASLD',
        'INH':'59',
        'size':1
    },
    {
        'mnemonic':'ASR',
        'EXT':'77 hh ll',
        'size':3
    },
    {
        'mnemonic':'ASRA',
        'INH':'47',
        'size':1
    },
    {
        'mnemonic':'ASRB',
        'INH':'57',
        'size':1
    },
    {
        'mnemonic':'BCLR',
        'DIR':'4D dd mm',
        'EXT':'1D hh ll mm',
        'size':3,
        'size:_ext':4
    },
    {
        'mnemonic':'BGND',
        'INH':'00',
        'size':1
    },
]