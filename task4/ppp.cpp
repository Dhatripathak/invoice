
#include <iostream>



template<typename A> void foo(A arg) { std::cout << "generic" << std::endl; } template>> void foo(int arg) { std::cout << "int" << std::endl; } template<> void foo (double arg) { std::cout << "double" << std::endl; }

int main() {

foo (char (42)); return 0;

}