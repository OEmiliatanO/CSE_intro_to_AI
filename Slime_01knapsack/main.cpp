#include <iostream>

using namespace std;

constexpr int maxn = 1000;

int w[maxn], v[maxn];
int dp[maxn];

int main()
{
	int n, W;
	cin >> n >> W;
	for (int i = 0; i < n; ++i)
		cin >> w[i];
	for (int i = 0; i < n; ++i)
		cin >> v[i];
	for (int i = 0; i < n; ++i)
		for (int j = W; j >= w[i]; --j)
			dp[j] = max(dp[j], dp[j-w[i]]+v[i]);

	cout << dp[W] << '\n';
	return 0;
}
