# Safetrace Sandbox

An environment to run computations on a remote server.
> This is still a WIP

#### Computations:
- Currently only supports computation in a precombiled `.exe` binary.
- The first command line argument passed into the executable will be the file path of the text file to write any computational outputs to.

#### Sample C++ Program: 
```c++
/*
    computationDemo.cpp
*/

#include <iostream>
#include <fstream>
using namespace std;

void do_computations () {
    int a = 5;
    int b = 3;
    return a + b;
}

int main(int argc, char* argv[])
{
    cout << "Any stdout logs will be found in the 'Logs File'" << endl;

    cerr << "Error logs will be found in the Logs File' as well" << endl;

    // the outputs file
    string outputsPath = argv[1];
    ofstream outputsFile;
    outputsFile.open (outputsPath);
    
    // do the actual computations
    int resultOfComputation = do_computations();

    // send the results to the output file stream
    outputsFile << "Computation Result: " << resultOfComputation << endl;
    
    // close the outputs file stream and end the program
    outputsFile.close();
    return 0;
}
```
To compile the above program:

    $ g++ -o computationDemo.exe computationDemo.cpp

<hr>

#### Use on local server:

    $ curl -F 'file=@<path-to-executable>' -O -J http://localhost:3000/run

Will download a `<name-of-executable>_ComputationResults.zip` file to the current directory containing 2 files:
- a `<name-of-executable>_ComputationResult.txt` file containing the results of the computations output

- a `<name-of-executable>_ComputationLogs.txt` file containing logged errors during computation, any stdout, and any stderr outputs from the computation process
