#include <iostream>
#include <fstream>
using namespace std;

int main(int argc, char* argv[])
{
    string resultsFilePath = argv[1];

    cout << "Logging with stdout Test Line 1" << endl;
    
    ofstream myfile;
    myfile.open (resultsFilePath);
    myfile << "The Results From Computations Should Be Written Here" << endl;
    myfile << "Another Line Of Computation Results...." << endl;
    
    cout << "Logging with stdout Test Line 2" << endl;
    
    myfile.close();
    
    cerr << "ERROR Logging with stderr" << endl;
    return 0;
}