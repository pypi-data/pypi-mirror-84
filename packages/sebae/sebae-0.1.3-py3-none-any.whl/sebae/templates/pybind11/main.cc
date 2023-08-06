#include <iostream>
#include "algo.h"

// Use this file to debug your C++ code
int main() {
    std::cout << add(1, 2) << std::endl;
    Calc calculator(0.1);
    std::cout << calculator.subtract(1, 2) << std::endl;
    return 0;
}