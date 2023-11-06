def m_match (code_inst):
    for monic in mnemonics:
        if code_inst == monic['mnemonic']:
            return monic
    return None

def d_match (code_inst:str):
    for index,d in enumerate(direc):
        if code_inst == d:
            return index
    return None

def get_xysp (xysp_str:str):
    n = ''
    if xysp_str == 'X':
        n = '00'
    elif xysp_str == 'Y':
        n = '01'
    elif xysp_str == 'SP':
        n = '10'
    elif xysp_str == 'PC':
        n = '11'
    return n

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
        'IDX':'A9'
    },
    {
        'mnemonic':'ADCB',
        'IMM':'C9 ii',
        'DIR':'D9 dd',
        'EXT':'F9 hh ll',
        'IDX':'E9'
    },
    {
        'mnemonic':'ADDA',
        'IMM':'8B ii',
        'DIR':'9B dd',
        'EXT':'BB hh ll',
        'IDX':'AB'
    },
    {
        'mnemonic':'ADDB',
        'IMM':'CB ii',
        'DIR':'DB dd',
        'EXT':'FB hh ll',
        'IDX':'EB'
    },
    {
        'mnemonic':'ADDD',
        'IMM':'C3 jj kk',
        'DIR':'D3 dd',
        'EXT':'F3 hh ll',
        'IDX':'E3'
    },
    {
        'mnemonic':'ANDA',
        'IMM':'84 ii',
        'DIR':'94 dd',
        'EXT':'B4 hh ll',
        'IDX':'A4'
    },
    {
        'mnemonic':'ANDB',
        'IMM':'C4 ii',
        'DIR':'D4 dd',
        'EXT':'F4 hh ll',
        'IDX':'E4'
    },
    {
        'mnemonic':'ANDCC',
        'IMM':'10 ii',
    },
    {
        'mnemonic':'ASL',
        'EXT':'78 hh ll',
        'IDX':'68'
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
        'IDX':'67'
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
        'IDX':'0D'
    },
    {
        'mnemonic':'BGND',
        'INH':'00',
    },
    {
        'mnemonic':'BNE',
        'REL':'26 rr'
    },
    {
        'mnemonic':'LBNE',
        'REL':'18 26 qq rr'
    },
    {
        'mnemonic':'JMP',
        'EXT':'06 hh ll',
        'IDX':'05'
    }
]

direc = [
    'START',
    'ORG',
    'END',
    'DC.B',
    'DC.W',
    'BSZ',
    'zmb',
    'FCB',
    'FCC',
    'FILL'
]