def match (code_inst):
    for monic in mnemonics:
        if code_inst == monic['mnemonic']:
            return monic
    return None

class AddrMd:
    INH = 0
    IMM = 1
    DIR = 3
    EXT = 4

mnemonics = [
    {
        'mnemonic':'ABA',
        'INH':'18 06',
    },
    {
        'mnemonic':'ABX',
        'INH':'1A B5',
    },
    {
        'mnemonic':'ABY',
        'INH':'19 ED',
    },
    {
        'mnemonic':'ADCA',
        'IMM':'89 ii',
        'DIR':'99 dd',
        'EXT':'B9 hh ll',
    },
    {
        'mnemonic':'ADCB',
        'IMM':'C9 ii',
        'DIR':'D9 dd',
        'EXT':'F9 hh ll',
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
    },
    {
        'mnemonic':'ANDCC',
        'IMM':'10 ii',
    },
    {
        'mnemonic':'ASL',
        'EXT':'78 hh ll',
    },
    {
        'mnemonic':'ASLA',
        'INH':'48',
    },
    {
        'mnemonic':'ASLB',
        'INH':'58',
    },
    {
        'mnemonic':'ASLD',
        'INH':'59',
    },
    {
        'mnemonic':'ASR',
        'EXT':'77 hh ll',
    },
    {
        'mnemonic':'ASRA',
        'INH':'47',
    },
    {
        'mnemonic':'ASRB',
        'INH':'57',
    },
    {
        'mnemonic':'BCLR',
        'DIR':'4D dd mm',
        'EXT':'1D hh ll mm',
    },
    {
        'mnemonic':'BGND',
        'INH':'00',
    },
]