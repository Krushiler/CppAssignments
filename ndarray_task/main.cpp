#include <vector>
#include <iostream>
#include "ndarray.cpp"

int main(int argc, char const *argv[])
{
    auto shape = std::vector<int>();
    shape.push_back(4);
    shape.push_back(4);
    auto array = NDArray<float>::random(shape);

    auto min = array.mean(1);

    array.print();
    std::cout << "\n\n";
    min.print();

    return 0;
}
