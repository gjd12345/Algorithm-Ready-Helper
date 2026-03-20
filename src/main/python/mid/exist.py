class Solution:
    def exist(self, board, word):
        m, n = len(board), len(board[0])
        def backtrack(i, j, k):
            if i < 0 or j < 0 or i >= m or j >= n or board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            temp = board[i][j]
            board[i][j] = '.'
            res = backtrack(i+1, j, k+1) or backtrack(i-1, j, k+1) or \
                  backtrack(i, j+1, k+1) or backtrack(i, j-1, k+1)
            board[i][j] = temp
            return res
        
        for i in range(m):
            for j in range(n):
                if backtrack(i, j, 0):
                    return True
        return False
