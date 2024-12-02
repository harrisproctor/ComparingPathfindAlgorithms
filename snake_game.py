import heapq

fuck = [[10,(1,12)]]
heapq.heapify(fuck)

heapq.heappush(fuck,[4,(12,12)])
heapq.heappush(fuck,[14,(19,12)])
heapq.heappush(fuck,[1,(19,19)])
heapq.heappush(fuck,[20,(1,1)])
print(fuck)
print(heapq.heappop(fuck))