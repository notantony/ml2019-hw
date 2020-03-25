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


int n;
long double k[107][107], y[107], t[107][107], lam[107], lamc[107];
long double c;

long double w[107], m[107];

long double get_b() {
	int nzi = 999;
	long double eps = 1e-5;
	for (int i = 0; i < n; i++) {
		if (lam[i] > eps && lam[i] < c - eps) {
			nzi = i;
		} else if (lam[i] > eps && nzi == 999) {
			nzi = -i;
		}
	}
	if (nzi < 0) {
		nzi = -nzi;
	}

	long double b = 0.0l;
	for (int i = 0; i < n; i++) {
		b += lam[i] * k[i][nzi] * y[i];
	}
	b -= y[nzi];
	return b;
}

long double get_res() {
	long double res = 0;
	for (int i = 0; i < n; i++) {
		res += -lam[i];
		for (int j = 0; j < n; j++) {
			res += lam[i] * lam[j] * t[i][j] * 0.5;
		}
	}
	return res;
}

long double f(long double x, long double a, long double b) {
	return a * x * x + b * x;
}

void upd(int i1, int i2) {
	long double lm1 = lam[i1], lm2 = lam[i2];
	long double s = lam[i1] * y[i1] + lam[i2] * y[i2];

	long double a = 0.5 * t[i1][i1] + 0.5 * t[i2][i2] - 0.5 * (t[i1][i2] + t[i2][i1]) * y[i2] * y[i1];
	long double b = -1.0l + y[i1] * y[i2] - t[i1][i1] * s * y[i2] + 0.5 * (t[i1][i2] + t[i2][i1]) * y[i1] * s;

	for (int i = 0; i < n; i++) {
		if (i != i1 && i != i2) {
			b += -0.5 * t[i1][i] * y[i1] * y[i2] * lam[i];
			b += -0.5 * t[i][i1] * y[i1] * y[i2] * lam[i];
			b += 0.5 * t[i][i2] * lam[i];
			b += 0.5 * t[i2][i] * lam[i];
		}
	}

	long double mn, mx;
	if (y[i1] * y[i2] > 0) {
		mn = max(s * y[i1] - c, 0.0l);
		mx = min(s * y[i1], c);
	} else {
		mn = max(-s * y[i1], 0.0l);
		mx = min(c - s * y[i1], c);
	}

	long double l1 = mn;
	long double l2 = mx;
	long double l3 = -b / 2.0l / a;
	if (l3 < mn || l3 > mx) {
		l3 = mn;
	}

	long double f1 = f(l1, a, b);
	long double f2 = f(l2, a, b);
	long double f3 = f(l3, a, b);

	if (f1 <= f2 && f1 <= f3) {
		lam[i2] = l1;
	} else if (f2 <= f1 && f2 <= f3) {
		lam[i2] = l2;
	} else {
		lam[i2] = l3;
	}
	lam[i1] = (s - y[i2] * lam[i2]) * y[i1];
}


vector<int> pos, neg;

void ini_lam(int tries) {
	for (int i = 0; i < n; i++) {
		w[i] = 0;
	}
	if (tries == 0) {
		for (int i = 0; i < n; i++) {
			lam[i] = 0;
		}
	} else if (tries == 1) {
		for (int i = 0; i < pos.size(); i++) {
			lam[pos[i]] = c / (long double)pos.size();
		}
		for (int i = 0; i < neg.size(); i++) {
			lam[neg[i]] = c / (long double)neg.size();
		}
	} else {
		for (int i = 0; i < n; i++) {
			lam[i] = 0;
		}
		//int k = rand() % min(pos.size(), neg.size());
		for (int i = 0; i < min(pos.size(), neg.size()); i++) {
			lam[pos[i]] = c;
			lam[neg[i]] = c;
		}
	}
}

void sol() {
	cin >> n;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cin >> k[i][j];
		}
		cin >> y[i];
		if (y[i] > 0) {
			pos.push_back(i);
		} else {
			neg.push_back(i);
		}
	}
	cin >> c;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			t[i][j] = k[i][j] * y[i] * y[j];
		}
	}

	vector<int> v;
	for (int i = 0; i < n; i++) {
		v.push_back(i);
	}
	vector<pair<int, int>> vv;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < i; j++) {
			vv.push_back(make_pair(i, j));
		}
	}

	long double mx = 1e9;

	for (int tries = 0; tries < 1; tries++) {
		/*ini_lam(tries);

		for (int steps = 0; steps < 1700; steps++) {
		random_shuffle(v.begin(), v.end());
		for (int i = 0; i + 1 < v.size(); i++) {
		upd(v[i], v[i + 1]);
		}
		if (get_res() < mx) {
		mx = get_res();
		for (int i = 0; i < n; i++) {
		lamc[i] = lam[i];
		}
		}
		}*/

		double qwe = 999;
		ini_lam(tries);
		for (int steps = 0; steps < 5000; steps++) {
			random_shuffle(vv.begin(), vv.end());
			double eps = 1;
			for (int i = 0; i < vv.size(); i++) {
				upd(vv[i].first, vv[i].second);
			}
			if (qwe != 999 && abs(get_res() - qwe) < eps) {
				break;
			}
			qwe = get_res();
			/*if (get_res() < mx) {
				mx = get_res();
				for (int i = 0; i < n; i++) {
					lamc[i] = lam[i];
				}
			}*/
		}
	}
	/*for (int i = 0; i < n; i++) {
		lam[i] = lamc[i];
	}*/

	for (int i = 0; i < n; i++) {
		assert(lam[i] >= 0 && lam[i] <= c);
		cout << abs(lam[i]) << '\n';
	}

	cout << -get_b();
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