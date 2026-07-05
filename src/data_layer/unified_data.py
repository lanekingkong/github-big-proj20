"""
统一数据层 - 结构化+非结构化数据无缝接入

解决SMEs数据分散问题，支持：
- 结构化数据（SQLite/PostgreSQL）
- 非结构化数据（PDF/Word/邮件/合同）
- 知识图谱缓存
- 向量存储
"""
import json
import logging
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from enum import Enum

logger=logging.getLogger(__name__)

class DataSourceType(Enum):
    SQL="sql"
    VECTOR="vector"
    GRAPH="graph"
    DOCUMENT="document"
    API="api"

@dataclass
class DataSource:
    """数据源定义"""
    name:str
    source_type:DataSourceType
    connection_string:str
    enabled:bool=True
    metadata:dict=None

class UnifiedDataLayer:
    """统一数据层——连接所有数据源"""

    def __init__(self,db_path:str="~/.aetherflow/data.db",vector_path:str="~/.aetherflow/vectors",kg_path:str="~/.aetherflow/kgraph"):
        self.db_path=Path(db_path).expanduser()
        self.vector_path=Path(vector_path).expanduser()
        self.kg_path=Path(kg_path).expanduser()
        self._sources:dict[str,DataSource]={}
        self._db_conn=None

        self._init_dirs()
        self._init_db()

    def _init_dirs(self):
        for p in [self.db_path.parent,self.vector_path,self.kg_path]:
            p.mkdir(parents=True,exist_ok=True)

    def _init_db(self):
        """初始化SQLite主数据库"""
        self._db_conn=sqlite3.connect(str(self.db_path))
        cursor=self._db_conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS data_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                source_type TEXT NOT NULL,
                connection_string TEXT,
                enabled INTEGER DEFAULT 1,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content_type TEXT,
                file_path TEXT,
                source TEXT,
                extracted_text TEXT,
                vector_id TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                key TEXT,
                value TEXT,
                embedding_id TEXT,
                importance REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS knowledge_triples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                object TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_memory_session ON memory_entries(session_id);
            CREATE INDEX IF NOT EXISTS idx_memory_key ON memory_entries(key);
            CREATE INDEX IF NOT EXISTS idx_kg_subject ON knowledge_triples(subject);
            CREATE INDEX IF NOT EXISTS idx_kg_object ON knowledge_triples(object);
        """)
        self._db_conn.commit()
        logger.info(f"数据层初始化完成: {self.db_path}")

    def register_source(self,source:DataSource)->bool:
        """注册数据源"""
        if source.name in self._sources:
            return False
        self._sources[source.name]=source

        cursor=self._db_conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO data_sources (name,source_type,connection_string,enabled,metadata) VALUES (?,?,?,?,?)",
            (source.name,source.source_type.value,source.connection_string,1 if source.enabled else 0,json.dumps(source.metadata or {}))
        )
        self._db_conn.commit()
        return True

    def store_document(self,title:str,file_path:str,content_type:str,extracted_text:str,source:str="",metadata:dict=None)->int:
        """存储文档"""
        cursor=self._db_conn.cursor()
        cursor.execute(
            "INSERT INTO documents (title,content_type,file_path,source,extracted_text,metadata) VALUES (?,?,?,?,?,?)",
            (title,content_type,file_path,source,extracted_text,json.dumps(metadata or {}))
        )
        self._db_conn.commit()
        return cursor.lastrowid

    def store_memory(self,session_id:str,key:str,value:str,importance:float=0.5)->int:
        """存储会话记忆"""
        cursor=self._db_conn.cursor()
        cursor.execute(
            "INSERT INTO memory_entries (session_id,key,value,importance) VALUES (?,?,?,?)",
            (session_id,key,value,importance)
        )
        self._db_conn.commit()
        return cursor.lastrowid

    def retrieve_memory(self,session_id:str,key:Optional[str]=None,limit:int=10)->list[dict]:
        """检索会话记忆"""
        cursor=self._db_conn.cursor()
        if key:
            cursor.execute(
                "SELECT * FROM memory_entries WHERE session_id=? AND key=? ORDER BY importance DESC,last_accessed DESC LIMIT ?",
                (session_id,key,limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM memory_entries WHERE session_id=? ORDER BY importance DESC,last_accessed DESC LIMIT ?",
                (session_id,limit)
            )
        columns=[desc[0] for desc in cursor.description]
        return [dict(zip(columns,row)) for row in cursor.fetchall()]

    def store_knowledge_triple(self,subject:str,predicate:str,obj:str,confidence:float=1.0,source:str="")->int:
        """存储知识图谱三元组"""
        cursor=self._db_conn.cursor()
        cursor.execute(
            "INSERT INTO knowledge_triples (subject,predicate,object,confidence,source) VALUES (?,?,?,?,?)",
            (subject,predicate,obj,confidence,source)
        )
        self._db_conn.commit()
        return cursor.lastrowid

    def query_knowledge(self,subject:Optional[str]=None,obj:Optional[str]=None,limit:int=50)->list[dict]:
        """查询知识图谱"""
        cursor=self._db_conn.cursor()
        if subject and obj:
            cursor.execute(
                "SELECT * FROM knowledge_triples WHERE subject=? AND object=? LIMIT ?",
                (subject,obj,limit)
            )
        elif subject:
            cursor.execute(
                "SELECT * FROM knowledge_triples WHERE subject=? LIMIT ?",
                (subject,limit)
            )
        elif obj:
            cursor.execute(
                "SELECT * FROM knowledge_triples WHERE object=? LIMIT ?",
                (obj,limit)
            )
        else:
            cursor.execute("SELECT * FROM knowledge_triples LIMIT ?",(limit,))
        columns=[desc[0] for desc in cursor.description]
        return [dict(zip(columns,row)) for row in cursor.fetchall()]

    def list_sources(self)->list[dict]:
        """列出所有数据源"""
        cursor=self._db_conn.cursor()
        cursor.execute("SELECT * FROM data_sources WHERE enabled=1")
        columns=[desc[0] for desc in cursor.description]
        return [dict(zip(columns,row)) for row in cursor.fetchall()]

    def get_stats(self)->dict:
        """获取数据层统计"""
        cursor=self._db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM memory_entries")
        mem_count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM knowledge_triples")
        kg_count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM data_sources")
        src_count=cursor.fetchone()[0]

        return {
            "documents":doc_count,
            "memory_entries":mem_count,
            "knowledge_triples":kg_count,
            "data_sources":src_count,
            "db_size_mb":round(self.db_path.stat().st_size/1024/1024,2) if self.db_path.exists() else 0,
        }

    def close(self):
        """关闭数据层连接"""
        if self._db_conn:
            self._db_conn.close()
            self._db_conn=None
            logger.info("数据层连接已关闭")
