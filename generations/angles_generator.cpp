#include <fstream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <ctime>

const double MIN_ANGLE = -M_PI;
const double MAX_ANGLE = M_PI;

double randomDoube(double min, double max)
{
    double f = (double) rand() / RAND_MAX;
    return min + f * (max - min);
}

double generateRandomAngle() {
    return randomDoube(MIN_ANGLE, MAX_ANGLE);
}

int main(int argc, char const *argv[])
{
    std::srand(std::time(NULL));
    generateRandomAngle();
    if (argc != 3) return -1;
    int anglesSetsCount = atoi(argv[1]);
    std::string fileName = argv[2];

    std::ofstream out(fileName);

    for (int i = 0; i < anglesSetsCount; i ++) {
        double angle1, angle2, angle3;
        angle1 = generateRandomAngle();
        angle2 = generateRandomAngle();
        angle3 = generateRandomAngle();

        out << angle1 << " " << angle2 << " " << angle3 << std::endl;
    }

    return 0;
}