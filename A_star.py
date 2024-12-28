import heapq

class State:
    def __init__(self, volumes, parent=None, move=None):
        self.volumes = volumes
        self.parent = parent
        self.move = move
        self.score = self.get_score()

    def get_score(self):
        return sum(self.volumes)

    def __lt__(self, other):
        return self.score < other.score

def get_neighbors(state, capacities):
    neighbors = []
    n = len(state.volumes)
    for i in range(n):
        for j in range(n):
            if i != j:
                volumes = state.volumes.copy()
                pour = min(volumes[i], capacities[j] - volumes[j])
                volumes[i] -= pour
                volumes[j] += pour
                if volumes != state.volumes:
                    neighbors.append(State(volumes, state, (i, j, pour)))
    return neighbors

def a_star(start, goal, capacities):
    open_list = [start]
    closed_list = set()
    while open_list:
        state = heapq.heappop(open_list)
        if state.volumes == goal:
            path = [state.move]
            while state.parent is not None:
                path.append(state.parent.move)
                state = state.parent
            return path[::-1]
        closed_list.add(tuple(state.volumes))
        for neighbor in get_neighbors(state, capacities):
            if tuple(neighbor.volumes) not in closed_list:
                heapq.heappush(open_list, neighbor)
    return None

def main():
    n, m, *capacities = map(int, input().split())
    start = State([0] * n)
    goal = None
    for i in range(1, max(capacities) + 1):
        for j in range(n):
            if capacities[j] == i:
                if goal is None:
                    goal = [0] * n
                goal[j] = i
                m -= i
                if m < 0:
                    print("Không có đáp án")
                    return
                break
        if m == 0:
            break
    if m > 0:
        print("Không có đáp án")
        return
    result = a_star(start, goal, capacities)
    if result is None:
        print("Không có đáp án")
    else:
        for move in result:
            print("Múc từ {} đến {} ({})".format(move[0], move[1], move[2]))

if __name__ == '__main__':
    main()
