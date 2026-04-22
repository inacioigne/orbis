def levenshtein(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[i + j if (i == 0 or j == 0) else 0 for j in range(n + 1)] for i in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

def edit_similarity(a: str, b: str) -> float:
    dist = levenshtein(a, b)
    return 1 - dist / max(len(a), len(b))