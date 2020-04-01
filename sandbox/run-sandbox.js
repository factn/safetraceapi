
const fs = require('fs');
const child_process = require('child_process');
const archiver = require('archiver');
const fsUtils = require('./fs-utils');

async function runSandbox (req, res, next) {
    let sandboxDir = './sandbox_I_' + Date.now() + '/';
    let resultStream =  null;
    let logStream = null;
    
    function deleteSandboxDirectory () {
        console.log('Removing Temporary Sandbox Directory');
        if (resultStream) resultStream.end();
        if (logStream) logStream.end();
        fsUtils.deleteDirectory(sandboxDir);
    }
    function onFinished (prefix) {
        return (e) => {
            deleteSandboxDirectory();
            if (e) {
                console.log(prefix + ' :: ' + e);
                res.status(e.status).send(e);
            }
        }
    }

    try {
        if(!req.files) 
            throw new Error('No file uploaded');
        
        // Use the name of the input field (i.e. "file") to retrieve the uploaded file
        // file.data: A buffer representation of your file, returns empty buffer in case useTempFiles option was set to true.
        let file = req.files.file;
        if (!file)
            throw new Error ('No File Specified With Key "file"');
        

        await fs.readdir('./', function(err, items) {
            console.log('PATH (BEFORE UPLOAD): ' + './');
            
            console.log(items);
            // for (var i=0; i<items.length; i++) {
            //     console.log(items[i]);
            // }
        });

        let computationPath = sandboxDir + file.name;
        
        console.log('Caching File... :: ' + computationPath);
        await file.mv(computationPath);

        console.log('Adjusting Primary Working Directory...');
        let pwd = (child_process.execSync(`pwd`) + sandboxDir.substring(1)).replace('\n', '');
        console.log('PWD: ' + pwd);

        console.log('Creating Output Streams...');
        let resultsPrefix = '.' + computationPath.substring(1).replace('.', '_');
        let resultsPath = resultsPrefix + "_ComputationResult.txt";
        let logsPath = resultsPrefix + "_ComputationLogs.txt";

        let resultsName = resultsPath.split('/').pop();
        let logsName = logsPath.split('/').pop();

        resultStream = fs.createWriteStream(resultsPath);
        await resultStream.end();

        logStream = fs.createWriteStream(logsPath);

        computationPath = pwd + file.name;
        console.log('Granting Permissions... :: ' + computationPath);
        // grant permissions
        child_process.execSync(`chmod +x ${computationPath}`);
        
        console.log('Awaiting...');
        await new Promise(resolve => setTimeout(resolve, 1000 * 1));

        await fs.readdir('./', function(err, items) {
            console.log('PATH: ' + './');
            
            console.log(items);
            // for (var i=0; i<items.length; i++) {
            //     console.log(items[i]);
            // }
        });
        await fs.readdir(sandboxDir, function(err, items) {
            console.log('PATH: ' + sandboxDir);
            console.log(items);
            // for (var i=0; i<items.length; i++) {
            //     console.log(items[i]);
            // }
        });


        console.log('Running : "' + path.resolve(__dirname, sandboxDir.substring(1) + file.name) + '"...');
        let stdOut, stdErr, err = null;
        let cp = child_process.execFile(
            path.resolve(__dirname, sandboxDir.substring(1) + file.name),
            // './'+file.name,
            [resultsName], 
            {
                cwd: pwd
            },
            (error, stdout, stderr) => {
                err = error;
                stdOut = stdout;
                stdErr = stderr;
            }
        );

        cp.on('close', async (code) => {
            try {

                console.log(`Computation Process Exited With Code: ${code}`);
                
                function writeLogsSection (section, obj) {
                    logStream.write(`[SANDBOX ${section}]: ===================================================\n\n`);
                    if (obj) logStream.write(obj.toString());
                    logStream.write('\n=====================================================================\n\n');
                }
                writeLogsSection ('ERRORS', err);
                writeLogsSection ('STDOUT', stdOut);
                writeLogsSection ('STDERR', stdErr);
                console.log('Done Writing Logs, Ending Stream...');
                logStream.end();
                logStream = resultStream = null;
                
                if (err) console.log('Sandbox Errors: ' + err);
                
                // archive results
                console.log('Archiving Results...');
                let archivePath = resultsPrefix + '_ComputationResults.zip';
                
                console.log('Creating Archive Stream...');
                let outputStream = fs.createWriteStream(archivePath);
                
                console.log('Creating Archiver...');
                var archive = archiver('zip', {
                    zlib: { level: 9 } // Sets the compression level.
                });
                
                // pipe archive data to the file
                archive.pipe(outputStream);
                
                // append a file
                function appendFile (path, name) {
                    console.log('Archiving: "' + path +  '" TO "' + name + '...');
                    archive.file(path, { name: name });
                }
                appendFile(resultsPath, resultsName);
                appendFile(logsPath, logsName);
                
                // handle errors
                archive.on('warning', onFinished('Archiver Warning'));
                archive.on('error', onFinished('Archiver Error'));
                // listen for all archive data to be written 'close' event is fired only when a file descriptor is involved
                outputStream.on('close', function() {
                    console.log('Finished Archiving, Size (bytes): ' + archive.pointer());
                    // send archive file as download response
                    res.download(archivePath, archivePath.split('/').pop(), onFinished('SUCCESS'));
                });
                
                console.log('Done Archiving...');
                // finalize the archive (ie we are done appending files but streams have to finish yet)
                // 'close', 'end' or 'finish' may be fired right after calling this method so register to them beforehand
                archive.finalize();
            }
            catch (e) {
                onFinished('Caught After Proccess Close')(e);
            }
        });
    }
    catch (err) {     
        onFinished('Caught')(err);   
    }
};

module.exports = runSandbox;