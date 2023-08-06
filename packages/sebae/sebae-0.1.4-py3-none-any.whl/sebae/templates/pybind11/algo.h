#pragma once

double add(double a, double b)
{
    return a + b;
}

class Calc {
private:
  double version;
public:
  Calc(double version) : version(version) {}
  double subtract(double a, double b) {
    return a - b;
  }

};