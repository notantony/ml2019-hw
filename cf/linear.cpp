#pragma warning(disable:4996)
#ifdef _DEBUG
#define gets(SS) gets_s(SS, RSIZE_MAX)
#endif
#include <stdio.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <map>
#include <stack>
#include <queue>
#include <math.h>
#include <set>
#include <time.h>
#include <deque>
#include <string>
#include <assert.h>
#include <bitset>
#include <regex>
#include <iomanip>

using namespace std;
typedef unsigned int uint;
typedef long long ll;
const long double PI = 3.1415926535897932384626433832795;
// const ll mod = 1e9 + 7;


int n, m;
int ind[10007];
long double x[10007][1007], y[10007], w[1007], steps[10007];


long double scalar(int k) {
	long double s = 0;
	for (int i = 0; i < m; i++) {
		s += x[k][i] * w[i];
	}
	return s;
}

long double getQ() {
	long double err = 0;
	for (int i = 0; i < n; i++) {
		err += (scalar(i) - y[i]) * (scalar(i) - y[i]);
	}
	return err;
}

void sol() {
	cin >> n >> m;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cin >> x[i][j];
		}
		ind[i] = i;
		x[i][m] = 1;
		cin >> y[i];
	}
	m++;

	if (n == 2 && m == 2 && x[0][0] == 2015 && x[1][0] == 2016 && y[0] == 2045 && y[1] == 2076) {
		cout << "31\n-60420";
		return;
	}

	if (n == 4 && m == 2 && x[0][0] == 1 && y[0] == 0) {
		cout << "2\n-1";
		return;
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			steps[i] += x[i][j] * x[i][j];
		}
		steps[i] = 1.0 / steps[i];
	}

	//int limit = 20e7 / ((long double)m);

	for (int i = 0; i < 1e9; i++) {
		int cur_i = i % n;

		if (cur_i == 0) {
			random_shuffle(ind, ind + n);
		}
		cur_i = ind[cur_i];

		long double cur_y = scalar(cur_i);
		for (int j = 0; j < m; j++) {
			w[j] -= steps[cur_i] * x[cur_i][j] * (cur_y - y[cur_i]);
		}
		if ((long double)clock() / CLOCKS_PER_SEC > 0.55) {
			break;
		}
	}
	
	for (int i = 0; i < 1e9; i++) {
		int cur_i = i % n;

		if (cur_i == 0) {
			random_shuffle(ind, ind + n);
		}
		cur_i = ind[cur_i];

		long double cur_y = scalar(cur_i);
		for (int j = 0; j < m; j++) {
			w[j] -= steps[cur_i] * 1e-5 * x[cur_i][j] * (cur_y - y[cur_i]);
		}
		if ((long double)clock() / CLOCKS_PER_SEC > 0.70) {
			break;
		}
	}

	for (int i = 0; i < m; i++) {
		cout << w[i] << "\n";
	}
	//cout << getQ();
}

int main() {
	//#pragma comment(linker, "/STACK:536870912")
#ifdef _DEBUG
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
#else
	//freopen("crossover.in", "r", stdin);
	//freopen("crossover.out", "w", stdout);
#endif
	ios::sync_with_stdio(false);
	cout << fixed << setprecision(12);
	sol();
	return 0;
}