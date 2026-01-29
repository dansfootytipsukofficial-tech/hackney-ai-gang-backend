from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re

router = APIRouter()

class WebSearchRequest(BaseModel):
    query: str
    max_results: int = 5

class WebSearchResponse(BaseModel):
    results: list[dict]

@router.post("/web/search", response_model=WebSearchResponse)
async def perform_web_search(request: WebSearchRequest):
    try:
        # Using DuckDuckGo instant answers API
        url = f"https://api.duckduckgo.com/?q={request.query}&format=json&no_html=1&skip_disambig=1"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        results = []

        # Extract instant answer if available
        if data.get('Answer'):
            results.append({
                'title': 'Instant Answer',
                'url': data.get('AnswerURL', ''),
                'snippet': data['Answer']
            })

        # Extract abstract if available
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', 'Abstract'),
                'url': data.get('AbstractURL', ''),
                'snippet': data['AbstractText']
            })

        # Extract related topics
        for topic in data.get('RelatedTopics', [])[:request.max_results]:
            if 'Text' in topic:
                results.append({
                    'title': topic.get('FirstURL', 'Related Topic'),
                    'url': topic.get('FirstURL', ''),
                    'snippet': topic['Text']
                })

        # If no results, provide a fallback
        if not results:
            results.append({
                'title': 'Search Results',
                'url': f"https://duckduckgo.com/?q={request.query}",
                'snippet': f"Search results for: {request.query}"
            })

        return WebSearchResponse(results=results[:request.max_results])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Web search error: {str(e)}")