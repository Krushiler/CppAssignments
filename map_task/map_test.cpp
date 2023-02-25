#include <fstream>
#include <map>
#include <chrono>
#include <map>

std::ofstream time_out("data/time_cpp.txt");
std::ofstream mem_out("data/mem_cpp.txt");

template <class Key, class Value>
unsigned long long map_capacity(const std::map<Key,Value> &map){
    unsigned long long cap = sizeof(map);
    for(typename std::map<Key,Value>::const_iterator it = map.begin(); it != map.end(); ++it){
        cap += sizeof(it->first);
        cap += sizeof(it->second);
    }
    return cap;
}

void test_map(int n) {
    auto map = std::map<int, int>();

    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; i ++) {
        map[i] = i;
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    
    std::chrono::duration<double, std::milli> elapsed = t2 - t1;

    time_out << n << " " << elapsed.count() << std::endl;
    mem_out << n << " " << map_capacity(map) << std::endl;
}

int main(int argc, char const *argv[])
{
    for (int i = 1; i <= 10000000; i *= 10) {
        test_map(i);
    }
}