.PHONY: install run test sample clean
install:
	pip install -r requirements.txt
run:
	uvicorn app.main:app --reload
test:
	pytest -q
sample:
	python scripts/create_sample_pdf.py
clean:
	rm -rf data/qdrant data/app.db data/sample_research_note.pdf
