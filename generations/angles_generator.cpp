#include <fstream>
#include <cmath>
#include <random>
#include <cstdlib>
#include <string>
#include <ctime>

const double MIN_ANGLE = -M_PI;
const double MAX_ANGLE = M_PI;

double generateRandomAngle() {
    std::random_device randomDevice;
    std::mt19937 generator(randomDevice());
    std::uniform_real_distribution<double> unif(MIN_ANGLE, MAX_ANGLE);

    double angle = unif(generator);
    return angle;
}

int main(int argc, char const *argv[])
{
    if (argc != 3) return -1;
    int anglesSetsCount = atoi(argv[1]);
    std::string fileName = argv[2];

    std::ofstream out(fileName);

    for (int i = 0; i < 10; i ++) {
        double angle1, angle2, angle3;
        angle1 = generateRandomAngle();
        angle2 = generateRandomAngle();
        angle3 = generateRandomAngle();

        out << angle1 << " " << angle2 << " " << angle3 << std::endl;
    }

    return 0;
}