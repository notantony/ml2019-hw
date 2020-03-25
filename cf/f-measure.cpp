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
const double PI = 3.1415926535897932384626433832795;
// const ll mod = 1e9 + 7;

int n;
int m[27][27];
double tp[27], fp[27], fn[27], p[27], p_res[27], recall[27], prec[27];

void sol() {
	cin >> n;
	double tp_all = 0.0;
	double all = 0.0;
	
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cin >> m[i][j];
		}
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (i != j) {
				fp[i] += m[j][i];
				fn[i] += m[i][j];
			}

			all += m[i][j];
		}
		tp_all += m[i][i];
		tp[i] = m[i][i];
	}

	for (int i = 0; i < n; i++) {
		p[i] = tp[i] + fn[i];
		p_res[i] = tp[i] + fp[i];
	}

	double macro_f = 0.0;
	double micro_recall = 0.0;
	double micro_prec = 0.0;
	for (int i = 0; i < n; i++) {
		double recall_i = tp[i] / p[i];
		double prec_i = tp[i] / p_res[i];

		if (tp[i] != 0) {
			macro_f += 2.0 * recall_i * prec_i / (recall_i + prec_i) * (p[i] / all);

			micro_recall += recall_i * p[i] / all;
			micro_prec += prec_i * p[i] / all;
		}
	}


	cout << micro_prec * micro_recall * 2.0 / (micro_prec + micro_recall) << '\n';
	cout << macro_f << '\n';
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
	cout << fixed << setprecision(10);
	sol();
	return 0;
}