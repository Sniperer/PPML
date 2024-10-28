#pragma once
#include "BigInt.hpp"
#include <vector>
#define Pair std::pair<BigInt, BigInt>
BigInt quickPow(BigInt base, BigInt exp, BigInt mod) {
  if (exp < 0) {
    if (base == 0)
      throw std::logic_error("Cannot divide by zero");
    return abs(base) == 1 ? base : 0;
  }
  if (exp == 0) {
    if (base == 0)
      throw std::logic_error("Zero cannot be raised to zero");
    return 1;
  }

  BigInt res = 1;
  while (exp > 0) {
    if (exp % 2 == 1)
      res = (res*base)%mod;
    base = (base*base)%mod;
    exp /= 2;
  }
  return res%mod;
}

bool isPrime(BigInt n) {
  if (n < 3 || n % 2 == 0) return n == 2;
  if (n % 3 == 0) return n == 3;
  BigInt u = n - 1, t = 0;
  while (u % 2 == 0) u /= 2, ++t;
  for (int i = 0; i < 5; ++i) {
    BigInt a = big_random() % (n - 3) + 2;
    BigInt v = quickPow(a, u, n);
    if (v == 1) continue;
    BigInt s;
    for (s = 0; s < t; ++s) {
      if (v == n - 1) break;
      v = v * v % n;
    }
    if (s == t) return 0;
  }
  return 1;
}

class EL {
public:
  EL(int sp): SecurityParameter(sp){
    while(true) {
      p = big_random(SecurityParameter);
      if (isPrime(p) && isPrime((p - 1)/2))
	break;
    }
    q = (p - 1)/2;
  }
  Pair gen(BigInt dd) {
    while(true) {
      g = big_random(SecurityParameter)%p;
      if (quickPow(g, 2, p) != 1 && quickPow(g, q, p) != 1)
	break;
    }
    d = dd;
    return std::make_pair(g, quickPow(g, d, p));
  }
  Pair Ogen(BigInt r) {
    return std::make_pair(g, quickPow(r, 2, p));
  }
  Pair enc(BigInt m, Pair pk) {
    BigInt r = big_random(SecurityParameter)%q;
    return std::make_pair(quickPow(pk.first,r,p), (quickPow(pk.second,r,p)*m)%p);
  }
  BigInt dec(Pair c, BigInt sk) {
    BigInt a;
    a = c.first;
    a = quickPow(a, sk, p);
    a = quickPow(a, p - 2, p);
    return (a*c.second)%p;
  }
private:
  int SecurityParameter;
  BigInt p;
  BigInt q;
  BigInt g;
  BigInt d;
};
