from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from config.qdrant import get_qdrant_client
from utils.embeddings import embed_text
import asyncio

async def crawl_medical_data():
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
    )
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator,
        max_depth=2,
        wait_for=5
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://pubmed.ncbi.nlm.nih.gov",
            config=config
        )
        chunks = [result.markdown[i:i+512] for i in range(0, len(result.markdown), 512)]
        client = get_qdrant_client()
        client.upload_collection(
            collection_name="medical_kb",
            documents=chunks,
            vectors=[embed_text(chunk) for chunk in chunks]
        )
        return len(chunks)