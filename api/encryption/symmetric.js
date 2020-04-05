const crypto = require('crypto');
const algorithm = 'aes-256-cbc';
const ivLength = 32;

function getKey () {
    return crypto.randomBytes(32).toString('hex');
}
function getIV () {
    return crypto.randomBytes(16).toString('hex');
}
function encryptData (data, key, ivString=null) {

    if (typeof data !== 'string')
        throw new Error('Symmetric Encrypting Requires String Data');
    
    let iv;
    if (!ivString) {
        iv = crypto.randomBytes(16);
        ivString = iv.toString('hex');
    }
    else {
        iv = Buffer.from(ivString, 'hex');
    }

    let cipher = crypto.createCipheriv(algorithm, Buffer.from(key, 'hex'), iv);
    let encrypted = Buffer.concat([cipher.update(data), cipher.final()]);
    return `${iv.toString('hex')}${encrypted.toString('hex')}`;
}
    
function splitIVData (encrypted) {
    return { iv: encrypted.substring(0, ivLength), data: encrypted.substring(ivLength) };
}

function decryptData(encrypted, key) {
    if (typeof encrypted !== 'string')
        throw new Error('Symmetric Decrypting Requires String Data');
    let { iv, data } = splitIVData(encrypted);
    let decipher = crypto.createDecipheriv(algorithm, Buffer.from(key, 'hex'), Buffer.from(iv, 'hex'));
    return Buffer.concat([decipher.update(Buffer.from(data, 'hex')), decipher.final()]).toString();
}

module.exports = { getKey, getIV, encryptData, decryptData, splitIVData };