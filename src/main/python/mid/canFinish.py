import sys

def canFinish(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    for dest, src in prerequisites:
        adj[src].append(dest)
    
    visited = [0] * numCourses # 0: unvisited, 1: visiting, 2: visited
    
    def has_cycle(u):
        if visited[u] == 1:
            return True
        if visited[u] == 2:
            return False
        
        visited[u] = 1
        for v in adj[u]:
            if has_cycle(v):
                return True
        visited[u] = 2
        return False
    
    for i in range(numCourses):
        if has_cycle(i):
            return False
    return True

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        numCourses = int(lines[0].strip())
        preLength = int(lines[1].strip())
        prerequisites = []
        for i in range(2, 2 + preLength):
            parts = lines[i].strip()
            if len(parts) >= 2:
                prerequisites.append([int(parts[0]), int(parts[1])])
        print(canFinish(numCourses, prerequisites))
