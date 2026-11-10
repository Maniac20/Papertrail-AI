import re
def reciprocal_rank(relevant_ids,ranked_ids):
    for rank,item in enumerate(ranked_ids,1):
        if item in relevant_ids: return 1.0/rank
    return 0.0
def recall_at_k(relevant_ids,ranked_ids,k):
    if not relevant_ids: return 0.0
    return len(set(ranked_ids[:k]) & set(relevant_ids))/len(relevant_ids)
def citation_coverage(answer):
    return 1.0 if re.search(r"\[[^\]]+,\s*p\.\s*\d+\]",answer) else 0.0
