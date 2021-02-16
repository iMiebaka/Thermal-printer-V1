var n = !isFinite(+number) ? 0 : +number,
s = '',
toFixedFix = function (n, decimals) {
    // return '' + (+(Math.round(n + 'e+' + decimals) + 'e-' + decimals));
    return '' + (+(Math.round(('' + n).indexOf('e') > 0 ? n : n + 'e+' + decimals) + 'e-' + decimals));
};