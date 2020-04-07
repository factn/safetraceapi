
const bcrypt = require('bcrypt');
const crypto = require('crypto');

function getRandomSalt() {
    let min = Number(process.env.BCRYPT_SALT_MIN);
    let max = Number(process.env.BCRYPT_SALT_MAX);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
async function hashStringRandom (string) {
    return (await bcrypt.hash(string, getRandomSalt()));
}
async function hashString (string) {
    return crypto.createHash('sha256').update(string).digest("hex");
}

module.exports = { hashString, hashStringRandom };