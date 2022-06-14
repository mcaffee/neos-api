from enum import Enum


class StatusEnum(str, Enum):
    OK = 'ok'
    FAILURE = 'failure'


class LiteralEnum(str, Enum):
    A = 'А'
    B = 'Б'
    V = 'В'
    G = 'Г'
    D = 'Д'
    YE = 'Е'
    ZH = 'Ж'
    Z = 'З'
    I = 'И'
    K = 'К'
    L = 'Л'
    M = 'М'
    N = 'Н'
    O = 'О'
    P = 'П'
    R = 'Р'
    S = 'С'
    T = 'Т'
    U = 'У'
    F = 'Ф'
    KH = 'Х'
    TS = 'Ц'
    CH = 'Ч'
    SH = 'Ш'
    Y = 'Ы'
    AE = 'Э'
    YU = 'Ю'
    YA = 'Я'
