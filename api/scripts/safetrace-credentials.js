const a_Encryption = require('../encryption/asymmetric');
const s_Encryption = require('../encryption/symmetric');
const hashing = require('../encryption/hashing');
const { v1 } = require('uuid');

function createSafetraceCredentials () {
    console.log('\nSAFETRACE_KEY=' + s_Encryption.getKey());
    console.log('\nSAFETRACE_IV=' + s_Encryption.getIV());
    console.log('\nSAFETRACE_API_KEY=' + v1());
    let keyPair = a_Encryption.getKeyPair();
    console.log('\nSAFETRACE_PUBLIC_KEY=' + keyPair.publicKey);
    console.log('\nSAFETRACE_PRIVATE_KEY=' + keyPair.privateKey);
}
// createSafetraceCredentials();

function getEncryptedLengths () {
    let k = s_Encryption.getKey();
    console.log('Symmetric Key Length: ' + k.length);
    let keyPair = a_Encryption.getKeyPair();
    console.log('Asymmetric Public Key Length: ' + keyPair.publicKey.length);
    console.log('Asymmetric Private Key Length: ' + keyPair.privateKey.length);
    let encryptedPrivateKey = s_Encryption.encryptData(keyPair.privateKey, k);
    console.log('Encrypted Asymmetric Private Key Length: ' + encryptedPrivateKey.length);   
    let apiKey = v1();
    let encryptedAPIKey = s_Encryption.encryptData(apiKey, k);
    console.log('Encrypted API Key Length: ' + encryptedAPIKey.length);   
    let assymetricallyEncryptedKey = a_Encryption.encryptData(k, keyPair.publicKey);
    console.log('Asymmetrically Encrypted Symmetric Key Length: ' + assymetricallyEncryptedKey.length);   
}
// getEncryptedLengths();

function testEncryptions () {
    let locationData = 'Union Square, NYC';
    let deviceKey = s_Encryption.getKey();
    let encryptedLocationData = s_Encryption.encryptData(locationData, deviceKey);
    let keyPairs = a_Encryption.getKeyPair();
    let encryptedDeviceKey = a_Encryption.encryptData(deviceKey, keyPairs.publicKey);
    let decryptedDeviceKey = a_Encryption.decryptData(encryptedDeviceKey, keyPairs.privateKey);
    let decryptedLocationData = s_Encryption.decryptData(encryptedLocationData, decryptedDeviceKey);
    console.log('Decrypted Data: ' + decryptedLocationData);
    console.log('Original Data: ' + locationData);
}
// testEncryptions();

const alphaNum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
function randomInt (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
function randomString (minLength, maxLength) {
    let l = randomInt(minLength, maxLength);
    let s = '';
    for (let i = 0; i < l; i++) 
        s += alphaNum[ randomInt(0, alphaNum.length - 1) ];
    return s;
}
async function testHashes () {
    for (let i = 0; i < 10; i++) {
        let hash = await hashing.hashString(randomString(5, 64));
        console.log(hash.length);
    }
}
// testHashes();


