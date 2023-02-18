#include <fstream>
#include <iostream>
#include <cmath>
#include <string>
#include <ctime>

int main(int argc, char const *argv[])
{
    if (argc != 2) return -1;
    std::string fileName = argv[1];
    
    std::ifstream fin(fileName);
    std::ofstream fout("proceed_"+fileName);

    while (!fin.eof() || !fin.fail())
    {
        double x, y, z;
        fin >> x >> y >> z;
        double angle = 2 * std::sin(x) * std::sin(y) + std::cos(z);
        std::cout << angle << std::endl;
        fout << angle << std::endl;
    }
    
    return 0;
}