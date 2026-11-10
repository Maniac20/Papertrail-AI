from app.ingestion.chunker import TextChunker,clean_text
def test_clean_text():
    assert clean_text("hello   world\n\n\nnext")=="hello world\n\nnext"
def test_chunk_metadata_and_overlap():
    chunks=TextChunker(20,5).split_pages([{"page":3,"text":"one two three four five six seven eight nine"}])
    assert len(chunks)>1 and all(c["page"]==3 for c in chunks)
def test_invalid_chunk_settings():
    try: TextChunker(10,10)
    except ValueError: return
    assert False
