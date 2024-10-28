#include "ElGamal.hpp"
#include <iostream>
#include <chrono>

using namespace std;
int main() {
  for(int i = 1; i < 100; ++i) {
    cout << big_random(2) << endl;
  }
  auto start = chrono::high_resolution_clock::now();
  EL e(20);
  auto stop = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::milliseconds> (stop - start);
  cout << "running time [ms]: " << duration.count() << endl;
  for(int i = 1; i < 100; ++i) {
    Pair pk = e.gen(i);
    Pair c = e.enc(i, pk);
    cout << e.dec(c, i) << endl;
  }
  return 0;
}
