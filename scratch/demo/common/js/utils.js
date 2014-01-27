/*
    -9007199254740990 to 9007199254740990
*/

function isInt(n) {
    return +n === n && !(n % 1);
}

/*
    -128 to 127
*/

function isInt8(n) {
    return +n === n && !(n % 1) && n < 0x80 && n >= -0x80;
}

/*
    -32768 to 32767
*/

function isInt16(n) {
    return +n === n && !(n % 1) && n < 0x8000 && n >= -0x8000;
}

/*
    -2147483648 to 2147483647
*/

function isInt32(n) {
    return +n === n && !(n % 1) && n < 0x80000000 && n >= -0x80000000;
}

/*
    0 to 9007199254740990
*/

function isUint(n) {
    return +n === n && !(n % 1) && n >= 0;
}

/*
    0 to 255
*/

function isUint8(n) {
    return +n === n && !(n % 1) && n < 0x100 && n >= 0;
}

/*
    0 to 65535
*/

function isUint16(n) {
    return +n === n && !(n % 1) && n < 0x10000 && n >= 0;
}

/*
    0 to 4294967295
*/

function isUint32(n) {
    return +n === n && !(n % 1) && n < 0x100000000 && n >= 0;
}

/*
    Any number including Infinity and -Infinity but not NaN
*/

function isFloat(n) {
    return +n === n;
}

/*
    Any number from -3.4028234e+38 to 3.4028234e+38 (Single-precision floating-point format)
*/

function isFloat32(n) {
    return +n === n && Math.abs(n) <= 3.4028234e+38;
}

/*
    Any number excluding Infinity and -Infinity and NaN (Number.MAX_VALUE = 1.7976931348623157e+308)
*/

function isFloat64(n) {
    return +n === n && Math.abs(n) <= 1.7976931348623157e+308;
}
