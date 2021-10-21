def spearman(diff: list):
    new_list = [abs(number) for number in diff]
    return sum(new_list)

def rank_changes(diff: list, n: int):
    changes = 0
    for i in range(n):
        if diff[i] != 0:
            changes+=1
    
    return changes