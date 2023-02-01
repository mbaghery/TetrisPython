class Scorer:
    _score_prefactors = {0: 0, 1: 1, 2: 3, 3: 5, 4: 8}

    def __init__(self, score: int, level: int) -> None:
        self._level = level
        self._score = score
        self._total_n_lines_cleared = 0

    @property
    def level(self) -> int:
        return self._level

    @property
    def score(self) -> int:
        return self._score

    def add_score(self, n_lines_cleared: int) -> None:
        self._total_n_lines_cleared += n_lines_cleared
        self._score += self._score_prefactors[
            n_lines_cleared] * 100 * self._level

        self._level += self._total_n_lines_cleared // 10
        self._total_n_lines_cleared = self._total_n_lines_cleared % 10
