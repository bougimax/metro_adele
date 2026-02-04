def levenshtein(
    u: str,
    v: str,
    cout_remplacement: int = 1,
    cout_insertion: int = 1,
    cout_suppression: int = 1,
) -> int:
    len_u, len_v = len(u), len(v)
    T = [
        [0 for _ in range(len_v + 1)] for _ in range(len_u + 1)
    ]  # T a |u| + 1 lignes et |v| + 1 colonnes
    for i in range(len_u):
        T[i][-1] = (len_u - i) * cout_insertion
    for j in range(len_v):
        T[-1][j] = (len_v - j) * cout_insertion
    for k in range(len_u + len_v, -1, -1):
        # On va parcourir par couple d'indices qui somment à k
        for j in range(min(k, len_v), -1, -1):
            i = k - j
            if i == len_u or j == len_v:
                continue
            if i > len_u:
                break
            if u[i] == v[j]:
                T[i][j] = T[i + 1][j + 1]
            else:
                T[i][j] = min(
                    cout_suppression + T[i + 1][j],
                    cout_suppression + T[i][j + 1],
                    cout_remplacement + T[i + 1][j + 1],
                )
    return T[0][0]


def levenshtein_linear_space(
    u: str,
    v: str,
    cout_remplacement: int = 1,
    cout_insertion: int = 1,
    cout_suppression: int = 1,
) -> int:
    len_u, len_v = len(u), len(v)
    current_line = [(len_v - j) * cout_insertion for j in range(len_v + 1)]
    for i in range(len_u - 1, -1, -1):
        new_line = [0 for _ in range(len_v + 1)]
        for j in range(len_v, -1, -1):
            if j == len_v:
                new_line[j] = (len_u - i) * cout_insertion
            else:
                if u[i] == v[j]:
                    new_line[j] = current_line[j + 1]
                else:
                    new_line[j] = min(
                        cout_suppression + current_line[j],
                        cout_suppression + new_line[j + 1],
                        cout_remplacement + current_line[j + 1],
                    )
        current_line = new_line
    return current_line[0]
