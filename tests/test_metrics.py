from app.evaluation.metrics import reciprocal_rank,recall_at_k,citation_coverage
def test_mrr(): assert reciprocal_rank({"yes"},["no","yes"])==0.5
def test_recall(): assert recall_at_k({"a","b"},["a","x","b"],2)==0.5
def test_citation(): assert citation_coverage("Claim [paper.pdf, p. 4]")==1.0
