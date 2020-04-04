const { encrypt, decrypt, PrivateKey } = require('eciesjs');

function getKeyPair () {
    let keyPair = new PrivateKey();
    return { 
        publicKey: keyPair.publicKey.toHex(), 
        privateKey: keyPair.toHex() 
    };
}
function encryptData (data, publicKey) {
    if (typeof data !== 'string')
        throw new Error('Asymmetric Encrypting Requires String Data');
    return encrypt(publicKey, data).toString('hex');
}
function decryptData(encrypted, privateKey) {
    if (typeof encrypted !== 'string')
        throw new Error('Asymmetric Decrypting Requires String Data');
    return decrypt(privateKey, Buffer.from(encrypted, 'hex')).toString();
}
module.exports = { getKeyPair, encryptData, decryptData };