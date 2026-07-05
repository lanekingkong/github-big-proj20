"""
测试 - 数据层
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.data_layer.unified_data import UnifiedDataLayer

@pytest.fixture
def data_layer():
    """创建临时数据层进行测试"""
    tmp_dir=tempfile.mkdtemp()
    db_path=os.path.join(tmp_dir,"test.db")
    dl=UnifiedDataLayer(db_path=db_path,vector_path=os.path.join(tmp_dir,"vectors"),kg_path=os.path.join(tmp_dir,"kgraph"))
    yield dl
    dl.close()
    import shutil
    shutil.rmtree(tmp_dir,ignore_errors=True)

def test_store_document(data_layer):
    doc_id=data_layer.store_document("test doc","/tmp/test.pdf","pdf","extracted text content","local")
    assert doc_id>0

def test_store_memory(data_layer):
    mem_id=data_layer.store_memory("session_1","key1","value1",0.8)
    assert mem_id>0

def test_retrieve_memory(data_layer):
    data_layer.store_memory("session_1","key_a","value_a",0.9)
    data_layer.store_memory("session_1","key_b","value_b",0.5)
    memories=data_layer.retrieve_memory("session_1")
    assert len(memories)>=2

def test_knowledge_triple(data_layer):
    triple_id=data_layer.store_knowledge_triple("Alice","works_at","AcmeCorp",0.95,"source1")
    assert triple_id>0
    results=data_layer.query_knowledge(subject="Alice")
    assert len(results)>=1

def test_get_stats(data_layer):
    data_layer.store_document("doc","/tmp/doc.pdf","pdf","text")
    data_layer.store_memory("s1","k1","v1")
    stats=data_layer.get_stats()
    assert stats["documents"]>=1
    assert stats["memory_entries"]>=1
