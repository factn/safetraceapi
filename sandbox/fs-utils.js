const fs = require('fs');

function deleteDirectory(path) {
    if ( fs.existsSync(path) ) {
        fs.readdirSync(path).forEach(
            (file) => {
                var curPath = path + "/" + file;
                if (fs.lstatSync(curPath).isDirectory()) 
                    deleteDirectory(curPath);
                else
                    fs.unlinkSync(curPath); // delete file
            }
        );
        fs.rmdirSync(path);
    }
};

module.exports = {
    deleteDirectory
};