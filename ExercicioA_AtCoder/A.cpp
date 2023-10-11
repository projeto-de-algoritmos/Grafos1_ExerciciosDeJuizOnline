#include <bits/stdc++.h>

using namespace std;

vector<bool> solve(int N, vector<pair<int, int>>& roads, vector<int>& heights) {
    vector<bool> isGood(N, true);

    for (auto& road : roads) {
        int A = road.first - 1;
        int B = road.second - 1;

        if (heights[A] <= heights[B]) {
            isGood[A] = false;
        }
        if (heights[B] <= heights[A]) {
            isGood[B] = false;
        }
    }

    return isGood;
}

int main() {
    ios::sync_with_stdio(false);

    long long N, M;
    cin >> N >> M;

    vector<int> heights(N);
    vector<pair<int, int>> roads;

    for (int i = 0; i < N; i++) {
        cin >> heights[i];
    }

    for (int i = 0; i < M; i++) {
        int A, B;
        cin >> A >> B;
        roads.emplace_back(A, B);
    }

    vector<bool> isGood = solve(N, roads, heights);

    int ans = 0;

    for (int i = 0; i < N; i++) {
        if (isGood[i]) {
            ans++;
        }
    }

    cout << ans << endl;

    return 0;
}
