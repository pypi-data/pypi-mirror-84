#include <iostream>

#include <mylib.hpp>

int main()
{
    std::cerr << "Hello! mylib::calculate() returned " << mylib::calculate() << std::endl;
    return 0;
}