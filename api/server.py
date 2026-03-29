#!/usr/bin/env python3
"""
Knowledge Base API Server
基于 wiki-local Node.js 模块的 RESTful API 封装
"""

import subprocess
import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Knowledge Base API",
    description="基于 wiki-local 的个人知识库 RESTful API",
    version="1.0.0"
)

# CORS 配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# wiki-local Node.js 脚本路径 (绝对路径)
WIKI_LOCAL_PATH = "/home/punkchang/.openclaw/workspace/skills/wiki-local/src/wiki-local.js"

# 数据存储根目录 (绝对路径)
DATA_ROOT = "/home/punkchang/.openclaw/workspace/knowledge-base/data/wiki"


# === Pydantic Models ===

class WikiNoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    relatedTo: List[str] = Field(default_factory=list)


class WikiNoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    relatedTo: Optional[List[str]] = None


class WikiNoteResponse(BaseModel):
    slug: str
    title: str
    content: str
    tags: List[str]
    relatedTo: List[str]


# === Node.js 代码模板 (使用特殊占位符) ===

NODE_WRAPPER_TEMPLATE = """
const fs = require('fs');
const path = require('path');
const { WikiLocal } = require('__WIKI_LOCAL_PATH__');

const wikiDir = '__ARTICLES_DIR__';
const indexFile = '__INDEX_FILE__';

// 确保目录存在
if (!fs.existsSync(wikiDir)) {
    fs.mkdirSync(wikiDir, { recursive: true });
}

const wiki = new WikiLocal({
    wikiDir: wikiDir,
    indexFile: indexFile
});

const action = '__ACTION__';
const params = JSON.parse('__PARAMS__');

try {
    let result;
    
    switch(action) {
        case 'add':
            result = wiki.add(params.title, params.content, params.tags || [], params.relatedTo || []);
            const content = wiki.get(result.slug);
            if (content) {
                const lines = content.split('\\n');
                const title = lines[0].replace('# ', '');
                const tagLine = lines[1];
                const relatedLine = lines[2];
                const tags = tagLine.replace('Tags: ', '').split(', ').filter(t => t);
                const relatedTo = relatedLine.replace('Related: ', '').split(', ').filter(r => r);
                const bodyStart = content.indexOf('\\n\\n');
                const bodyContent = bodyStart > -1 ? content.substring(bodyStart + 2) : '';
                result = { ...result, title, tags, relatedTo, content: bodyContent };
            }
            break;
            
        case 'get':
            const get_content = wiki.get(params.slug);
            if (!get_content) throw new Error('Not found');
            const get_lines = get_content.split('\\n');
            const get_title = get_lines[0].replace('# ', '');
            const get_tagLine = get_lines[1];
            const get_relatedLine = get_lines[2];
            const get_tags = get_tagLine.replace('Tags: ', '').split(', ').filter(t => t);
            const get_relatedTo = get_relatedLine.replace('Related: ', '').split(', ').filter(r => r);
            const get_bodyStart = get_content.indexOf('\\n\\n');
            const get_bodyContent = get_bodyStart > -1 ? get_content.substring(get_bodyStart + 2) : '';
            result = { slug: params.slug, title: get_title, tags: get_tags, relatedTo: get_relatedTo, content: get_bodyContent };
            break;
            
        case 'search':
            result = wiki.search(params.query).map(item => ({
                ...item,
                title: item.title || item.slug
            }));
            break;
            
        case 'backlinks':
            result = wiki.backlinks(params.slug);
            break;
            
        case 'stats':
            result = wiki.stats();
            break;
            
        case 'list':
            try {
                const list_index = JSON.parse(fs.readFileSync(indexFile, 'utf8'));
                result = Object.entries(list_index).map(([slug, meta]) => ({
                    slug, title: meta.title, tags: meta.tags || [], relatedTo: meta.relatedTo || []
                }));
            } catch {
                result = [];
            }
            break;
            
        case 'delete':
            const del_file = path.join(wikiDir, params.slug + '.md');
            if (fs.existsSync(del_file)) {
                fs.unlinkSync(del_file);
                try {
                    const del_index = JSON.parse(fs.readFileSync(indexFile, 'utf8'));
                    delete del_index[params.slug];
                    fs.writeFileSync(indexFile, JSON.stringify(del_index, null, 2));
                } catch (e) {}
            }
            result = { deleted: params.slug };
            break;
            
        case 'update':
            const upd_existing = wiki.get(params.slug);
            if (!upd_existing) throw new Error('Not found');
            const upd_lines = upd_existing.split('\\n');
            let upd_currentTitle = upd_lines[0].replace('# ', '');
            let upd_currentTags = (upd_lines[1] || 'Tags: ').replace('Tags: ', '').split(', ').filter(t => t);
            let upd_currentRelatedTo = (upd_lines[2] || 'Related: ').replace('Related: ', '').split(', ').filter(r => r);
            const upd_bodyStart = upd_existing.indexOf('\\n\\n');
            let upd_currentContent = upd_bodyStart > -1 ? upd_existing.substring(upd_bodyStart + 2) : '';
            
            if (params.title) upd_currentTitle = params.title;
            if (params.tags !== undefined) upd_currentTags = params.tags;
            if (params.relatedTo !== undefined) upd_currentRelatedTo = params.relatedTo;
            if (params.content !== undefined) upd_currentContent = params.content;
            
            const upd_oldFile = path.join(wikiDir, params.slug + '.md');
            if (fs.existsSync(upd_oldFile)) fs.unlinkSync(upd_oldFile);
            
            result = wiki.add(upd_currentTitle, upd_currentContent, upd_currentTags, upd_currentRelatedTo);
            const upd_newContent = wiki.get(result.slug);
            if (upd_newContent) {
                const upd_lines2 = upd_newContent.split('\\n');
                const upd_title2 = upd_lines2[0].replace('# ', '');
                const upd_tagLine2 = upd_lines2[1];
                const upd_relatedLine2 = upd_lines2[2];
                const upd_tags2 = upd_tagLine2.replace('Tags: ', '').split(', ').filter(t => t);
                const upd_relatedTo2 = upd_relatedLine2.replace('Related: ', '').split(', ').filter(r => r);
                const upd_bodyStart2 = upd_newContent.indexOf('\\n\\n');
                const upd_bodyContent2 = upd_bodyStart2 > -1 ? upd_newContent.substring(upd_bodyStart2 + 2) : '';
                result = { ...result, title: upd_title2, tags: upd_tags2, relatedTo: upd_relatedTo2, content: upd_bodyContent2 };
            }
            break;
            
        default:
            throw new Error('Unknown action: ' + action);
    }
    
    console.log(JSON.stringify({ success: true, result }));
} catch (error) {
    console.log(JSON.stringify({ error: error.message }));
}
"""


def run_wiki_local(action: str, **kwargs) -> dict:
    """调用 wiki-local Node.js 模块执行操作"""
    params_json = json.dumps(kwargs, ensure_ascii=False)
    
    node_code = (NODE_WRAPPER_TEMPLATE
        .replace('__WIKI_LOCAL_PATH__', WIKI_LOCAL_PATH)
        .replace('__ARTICLES_DIR__', os.path.join(DATA_ROOT, "articles"))
        .replace('__INDEX_FILE__', os.path.join(DATA_ROOT, "index.json"))
        .replace('__ACTION__', action)
        .replace('__PARAMS__', params_json.replace("'", "'\\''")))
    
    cmd = ["node", "-e", node_code]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout.strip()
        if not output:
            raise HTTPException(status_code=500, detail=f"Empty response. stderr: {result.stderr}")
            
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON response: {output}\nParse error: {e}")
        
        if "error" in data:
            raise HTTPException(status_code=404 if "Not found" in data["error"] else 500, 
                              detail=data["error"])
            
        return data.get("result", {})
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Request timeout")


# === API Endpoints ===

@app.get("/")
async def root():
    """API 健康检查"""
    return {"status": "ok", "service": "Knowledge Base API"}


# 固定路径路由（必须放在通配符路由之前）
@app.post("/api/wiki/add", response_model=WikiNoteResponse)
async def add_note(note: WikiNoteCreate):
    """添加新笔记"""
    result = run_wiki_local(
        "add",
        title=note.title,
        content=note.content,
        tags=note.tags,
        relatedTo=note.relatedTo
    )
    return WikiNoteResponse(**result)


@app.get("/api/wiki/search")
async def search_notes(query: str, limit: int = 20):
    """全文搜索笔记"""
    results = run_wiki_local("search", query=query)
    return {"query": query, "results": results[:limit]}


@app.get("/api/wiki/list")
async def list_notes(limit: int = 20, offset: int = 0):
    """获取笔记列表（支持分页）"""
    all_notes = run_wiki_local("list")
    paginated = all_notes[offset:offset + limit]
    return {
        "notes": paginated, 
        "limit": limit, 
        "offset": offset,
        "total": len(all_notes)
    }


@app.get("/api/wiki/stats")
async def get_stats():
    """获取统计信息"""
    result = run_wiki_local("stats")
    return result


# 通配符路由（放在最后）
@app.get("/api/wiki/{slug}", response_model=WikiNoteResponse)
async def get_note(slug: str):
    """获取单篇笔记内容"""
    try:
        result = run_wiki_local("get", slug=slug)
        return WikiNoteResponse(**result)
    except HTTPException as e:
        if "Not found" in str(e.detail):
            raise HTTPException(status_code=404, detail=f"Note '{slug}' not found")
        raise


@app.put("/api/wiki/{slug}", response_model=WikiNoteResponse)
async def update_note(slug: str, note: WikiNoteUpdate):
    """更新笔记内容"""
    params = {"slug": slug}
    if note.title is not None:
        params["title"] = note.title
    if note.content is not None:
        params["content"] = note.content
    if note.tags is not None:
        params["tags"] = note.tags
    if note.relatedTo is not None:
        params["relatedTo"] = note.relatedTo
        
    result = run_wiki_local("update", **params)
    return WikiNoteResponse(**result)


@app.delete("/api/wiki/{slug}")
async def delete_note(slug: str):
    """删除笔记"""
    run_wiki_local("delete", slug=slug)
    return {"message": "Deleted successfully", "slug": slug}


@app.get("/api/wiki/backlinks/{slug}", response_model=List[dict])
async def get_backlinks(slug: str):
    """获取反向链接（哪些笔记链接到了当前笔记）"""
    result = run_wiki_local("backlinks", slug=slug)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
