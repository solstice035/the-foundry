#!/usr/bin/env python3
"""
Epic 1.2: Trend Scout - Normalization & Scoring

Processes raw trends from Epic 1.1 output and produces:
- trends-summary.json (top 15, compact for Spec Writer)
- trends-full/ directory (verbose per-trend details for debugging)

Implements:
- Engagement normalization (HN points, Reddit score → 0-100)
- Cross-source deduplication (URL exact + fuzzy title >70%)
- Auto-filters (political/crypto/proprietary → reject)
- Buildability scoring (5 dimensions, 0-2 each, 0-10 total)
- Auto-modifiers (+1 API mention, -2 ML training, -1 deployment infra)
- Cross-source amplification (1.3x for 2 sources, 2.0x for 4+)
- Two-tier schema output
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse, urljoin


# ============================================================================
# Configuration
# ============================================================================

# Auto-filter keywords (instant reject)
POLITICAL_KEYWORDS = {
    'election', 'biden', 'trump', 'conservative', 'liberal',
    'republican', 'democrat', 'congress', 'senate', 'politician',
    'political', 'politics', 'maga', 'woke'
}

CRYPTO_KEYWORDS = {
    'bitcoin', 'ethereum', 'nft', 'web3', 'crypto', 'cryptocurrency',
    'blockchain', 'defi', 'token', 'solana', 'mining'
}

PROPRIETARY_KEYWORDS = {
    # These indicate builds that need paid/proprietary infrastructure
    # Note: "openai api" is checked as a phrase, not individual words
}

PROPRIETARY_PHRASES = [
    'openai api', 'aws lambda', 'aws infrastructure',
]

# Auto-filter: reject trends matching these categories
AUTO_FILTER_CATEGORIES = {
    'political': POLITICAL_KEYWORDS,
    'crypto': CRYPTO_KEYWORDS,
}

# API mentions that boost buildability (+1)
API_MENTIONS = [
    'github api', 'hn api', 'hacker news api', 'reddit api',
    'twitter api', 'stripe api', 'spotify api', 'openweather',
    'rest api', 'graphql', 'public api', 'free api',
    'rss', 'json endpoint', 'json api', 'webhook',
]

# ML training signals (-2)
ML_TRAINING_SIGNALS = [
    'ml training', 'machine learning training', 'train a model',
    'fine-tune', 'fine tune', 'finetuning', 'training data',
    'neural network', 'deep learning model', 'train the',
    'gpu training', 'model training',
]

# Deployment infrastructure signals (-1)
DEPLOYMENT_SIGNALS = [
    'requires deployment', 'deploy to', 'kubernetes', 'docker compose',
    'cloud infrastructure', 'server setup', 'hosting required',
    'aws', 'gcp', 'azure', 'heroku',
]

# Stop words for keyword extraction
STOP_WORDS = {
    'a', 'an', 'the', 'for', 'with', 'using', 'from', 'to',
    'in', 'on', 'at', 'by', 'of', 'is', 'are', 'was', 'were',
    'and', 'or', 'but', 'not', 'its', 'it', 'this', 'that',
    'has', 'had', 'have', 'been', 'being', 'will', 'would',
    'could', 'should', 'may', 'might', 'can', 'do', 'does',
    'did', 'just', 'about', 'how', 'why', 'what', 'when',
    'where', 'who', 'which', 'more', 'some', 'any', 'all',
    'than', 'then', 'also', 'very', 'too', 'now', 'here',
    'there', 'your', 'you', 'they', 'them', 'their', 'our',
    'his', 'her', 'she', 'him', 'my', 'me', 'we', 'us',
    'ive', 'youre', 'im', 'dont', 'cant', 'wont', 'isnt',
}


# ============================================================================
# Engagement Normalization
# ============================================================================

def normalize_engagement(value: float, source: str) -> float:
    """
    Normalize engagement to 0-100 scale.
    
    Formulas from design docs:
    - HN points: min(100, points / 5)
    - Reddit score: min(100, score / 10)
    - X retweets: min(100, retweets / 2)
    """
    if source == 'hn':
        return min(100.0, value / 5.0)
    elif source == 'reddit':
        return min(100.0, value / 10.0)
    elif source == 'x':
        return min(100.0, value / 2.0)
    else:
        return min(100.0, value / 10.0)


# ============================================================================
# Keyword Extraction & Deduplication
# ============================================================================

def extract_keywords(text: str) -> Set[str]:
    """Extract keywords from text for fuzzy matching."""
    clean = re.sub(r'[^a-z0-9\s]', '', text.lower())
    words = clean.split()
    return {w for w in words if w not in STOP_WORDS and len(w) > 2}


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def normalize_url(url: str) -> str:
    """Normalize URL for comparison (strip query params, fragments, trailing slash)."""
    if not url:
        return ''
    parsed = urlparse(url)
    # Keep scheme, netloc, path only
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')
    return normalized.lower()


def deduplicate_trends(trends: List[Dict]) -> List[Dict]:
    """
    Cross-source deduplication.
    
    Matches by:
    1. Exact URL match (normalized)
    2. Fuzzy title match (Jaccard similarity > 70%)
    
    Merges duplicates: combines sources, uses highest engagement, applies amplification.
    """
    merged = []
    url_index = {}  # normalized_url -> index in merged
    
    for trend in trends:
        norm_url = normalize_url(trend.get('source_url', ''))
        
        # Check exact URL match
        matched_idx = None
        if norm_url and norm_url in url_index:
            matched_idx = url_index[norm_url]
        
        # Check fuzzy title match if no URL match
        if matched_idx is None:
            trend_keywords = extract_keywords(trend.get('title', '') + ' ' + trend.get('raw_title', ''))
            for idx, existing in enumerate(merged):
                existing_keywords = extract_keywords(
                    existing.get('title', '') + ' ' + existing.get('raw_title', '')
                )
                similarity = jaccard_similarity(trend_keywords, existing_keywords)
                if similarity > 0.70:
                    matched_idx = idx
                    break
        
        if matched_idx is not None:
            # Merge into existing
            existing = merged[matched_idx]
            
            # Add source info
            if 'all_sources' not in existing:
                existing['all_sources'] = [{
                    'source': existing['source'],
                    'source_url': existing.get('source_url', ''),
                    'engagement_value': existing['engagement_value'],
                    'engagement_metric': existing.get('engagement_metric', ''),
                    'raw_data': existing.get('raw_data', {}),
                }]
            
            existing['all_sources'].append({
                'source': trend['source'],
                'source_url': trend.get('source_url', ''),
                'engagement_value': trend['engagement_value'],
                'engagement_metric': trend.get('engagement_metric', ''),
                'raw_data': trend.get('raw_data', {}),
            })
            
            # Use highest engagement
            if trend['engagement_value'] > existing['engagement_value']:
                existing['engagement_value'] = trend['engagement_value']
                existing['engagement_metric'] = trend.get('engagement_metric', '')
                existing['source'] = trend['source']  # Primary source = highest engagement
            
            # Track source count
            sources = set()
            for s in existing['all_sources']:
                sources.add(s['source'])
            existing['source_count'] = len(sources)
        else:
            # New unique trend
            trend['source_count'] = 1
            if 'all_sources' not in trend:
                trend['all_sources'] = [{
                    'source': trend['source'],
                    'source_url': trend.get('source_url', ''),
                    'engagement_value': trend['engagement_value'],
                    'engagement_metric': trend.get('engagement_metric', ''),
                    'raw_data': trend.get('raw_data', {}),
                }]
            merged.append(trend)
            if norm_url:
                url_index[norm_url] = len(merged) - 1
    
    return merged


# ============================================================================
# Auto-Filters
# ============================================================================

def check_auto_filters(trend: Dict) -> List[str]:
    """
    Check if trend should be auto-filtered (rejected).
    
    Returns list of triggered filter reasons, empty if trend passes.
    """
    triggered = []
    text = (trend.get('title', '') + ' ' + trend.get('raw_title', '') + ' ' + trend.get('summary', '')).lower()
    
    # Political keywords
    for kw in POLITICAL_KEYWORDS:
        if kw in text:
            triggered.append(f"political: '{kw}' found")
            break
    
    # Crypto keywords
    for kw in CRYPTO_KEYWORDS:
        if kw in text:
            triggered.append(f"crypto: '{kw}' found")
            break
    
    # Proprietary phrases
    for phrase in PROPRIETARY_PHRASES:
        if phrase in text:
            triggered.append(f"proprietary: '{phrase}' found")
            break
    
    return triggered


# ============================================================================
# Auto-Modifiers
# ============================================================================

def calculate_auto_modifiers(trend: Dict) -> Tuple[int, List[str]]:
    """
    Calculate auto-modifiers for buildability score.
    
    Returns (modifier_total, list_of_reasons).
    """
    modifier = 0
    reasons = []
    text = (trend.get('title', '') + ' ' + trend.get('raw_title', '') + ' ' + trend.get('summary', '')).lower()
    
    # +1 if specific API mentioned
    for api in API_MENTIONS:
        if api in text:
            modifier += 1
            reasons.append(f"+1: {api} mentioned")
            break  # Only apply once
    
    # -2 if ML training required
    for signal in ML_TRAINING_SIGNALS:
        if signal in text:
            modifier -= 2
            reasons.append(f"-2: ML training signal '{signal}'")
            break
    
    # -1 if deployment infrastructure required
    for signal in DEPLOYMENT_SIGNALS:
        if signal in text:
            modifier -= 1
            reasons.append(f"-1: deployment infrastructure '{signal}'")
            break
    
    return modifier, reasons


# ============================================================================
# Buildability Scoring (Heuristic-based)
# ============================================================================

def score_buildability(trend: Dict) -> Tuple[int, Dict[str, int], str]:
    """
    Score buildability across 5 dimensions (0-2 each, 0-10 total).
    
    Uses heuristic analysis of title/summary/category.
    Returns (total_score, breakdown_dict, reasoning_string).
    """
    text = (trend.get('title', '') + ' ' + trend.get('raw_title', '') + ' ' + trend.get('summary', '')).lower()
    category = trend.get('category', '').lower()
    
    # Detect non-buildable content (news, essays, discussions, entertainment)
    non_buildable_signals = [
        'years later', 'lied to', 'testimony', 'going down',
        'stock', 'dumps', 'bill requires', 'claims of',
        'tv show', 'drama', 'best drama', 'documentary',
        'progress report', 'is down', 'is now', 'generally available',
        'the future of', 'the only moat', 'adoption and',
        'productivity paradox', 'helped save', 'thank hn',
        'so tired', 'anyone else having', 'slow year',
        'laid-off', 'laid off', 'unite', 'freelanc',
        'upwork', 'fiverr', 'imposter syndrome',
        'red flag', 'echo chamber', 'slashdot',
        'dying', 'drives from', 'seagate',
        'promo code', 'discount', 'coupon', 'verified',
    ]
    is_non_buildable = any(sig in text for sig in non_buildable_signals)
    
    # Also detect pure news/opinion by category
    news_categories = ['story']  # Plain HN stories are often news/opinions
    is_news_category = category in news_categories and not any(
        kw in text for kw in ['show hn', 'built', 'launch', 'tool', 'cli', 'api', 'app',
                               'library', 'framework', 'server', 'editor', 'generator',
                               'alternative', 'open source', 'open-source', 'client']
    )
    
    # Dimension 1: API Availability (0-2)
    api_score = 1  # Default: moderate
    api_reason = "Default moderate availability"
    
    api_positive = ['api', 'json', 'rss', 'cli', 'command line', 'terminal',
                    'open source', 'open-source', 'github', 'npm', 'pip',
                    'public data', 'scraping', 'webhook']
    api_negative = ['proprietary', 'private', 'paywall', 'closed source',
                    'no api', 'manual', 'hardware']
    
    if is_non_buildable or is_news_category:
        api_score = 0
        api_reason = "Non-buildable content, API availability N/A"
    elif any(kw in text for kw in api_positive):
        api_score = 2
        api_reason = "Public API/data or CLI tool indicated"
    elif any(kw in text for kw in api_negative):
        api_score = 0
        api_reason = "Proprietary/closed data source"
    
    if category == 'show_hn' and not (is_non_buildable or is_news_category):
        api_score = max(api_score, 2)
        api_reason = "Show HN = proven buildable with available APIs"
    
    # Dimension 2: Scope Clarity (0-2)
    scope_score = 1  # Default: moderate
    scope_reason = "Moderate scope clarity"
    
    if is_non_buildable or is_news_category:
        scope_score = 0
        scope_reason = "Non-buildable content (news/discussion/entertainment)"
    
    # Clear scope indicators
    scope_clear = ['generator', 'converter', 'checker', 'tracker', 'monitor',
                   'dashboard', 'viewer', 'editor', 'parser', 'formatter',
                   'linter', 'scanner', 'analyzer', 'calculator', 'finder',
                   'manager', 'organizer', 'compiler', 'emulator', 'server',
                   'alternative to', 'replacement for', 'client for']
    scope_vague = ['better', 'improve', 'future of', 'thoughts on',
                   'discussion', 'opinion', 'rant', 'anyone else',
                   'is there', 'how do you', 'why is', 'what do you think']
    
    if not (is_non_buildable or is_news_category):
        if any(kw in text for kw in scope_clear):
            scope_score = 2
            scope_reason = "Clear feature/tool type in title"
        elif any(kw in text for kw in scope_vague):
            scope_score = 0
            scope_reason = "Vague/discussion post, no clear buildable scope"
    
    # Dimension 3: Time Confidence (0-2)
    time_score = 1  # Default: moderate
    time_reason = "Moderate time confidence"
    
    if is_non_buildable or is_news_category:
        time_score = 0
        time_reason = "Non-buildable content, time estimate N/A"
    
    # High confidence: simple tools
    time_high = ['cli', 'command line', 'terminal', 'script', 'simple',
                 'tiny', 'minimal', 'single', 'lightweight', 'small',
                 'bot', 'webhook', 'static site']
    time_low = ['real-time', 'realtime', 'collaborative', 'distributed',
                'enterprise', 'platform', 'marketplace', 'social network',
                'operating system', 'kernel', 'browser engine', 'database engine',
                'compiler', 'emulator', 'game engine', '3d render', 'video edit',
                'streaming server', 'mobile app', 'ios app', 'android app']
    
    if not (is_non_buildable or is_news_category):
        if any(kw in text for kw in time_high):
            time_score = 2
            time_reason = "Simple/CLI tool, high confidence in 4-6h build"
        elif any(kw in text for kw in time_low):
            time_score = 0
            time_reason = "Complex architecture, unlikely buildable in 4-6h"
    
    # Dimension 4: Differentiation (0-2)
    diff_score = 1  # Default: moderate
    diff_reason = "Moderate differentiation"
    
    # Novel signals
    diff_novel = ['first', 'novel', 'new approach', 'unique', 'never before',
                  'innovative', 'experimental', 'unconventional', 'niche']
    diff_saturated = ['todo', 'to-do', 'task manager', 'note taking',
                      'blog platform', 'chat app', 'weather app',
                      'password manager', 'bookmark manager', 'url shortener']
    
    if is_non_buildable or is_news_category:
        diff_score = 0
        diff_reason = "Non-buildable content"
    elif any(kw in text for kw in diff_novel) or category == 'show_hn':
        diff_score = 2 if category == 'show_hn' else min(2, diff_score + 1)
        diff_reason = "Novel concept or Show HN (proven interest)"
    
    if not (is_non_buildable or is_news_category) and any(kw in text for kw in diff_saturated):
        diff_score = 0
        diff_reason = "Saturated category"
    
    # Dimension 5: Output Type (0-2)
    # 2 = CLI/API/static site (immediately visible)
    # 1 = web app (can demo)
    # 0 = mobile/browser ext/infra (hard to show)
    output_score = 1  # Default: moderate
    output_reason = "Standard output type"
    
    if is_non_buildable or is_news_category:
        output_score = 0
        output_reason = "Non-buildable content"
    
    output_great = ['cli', 'command line', 'terminal', 'tui', 'api',
                    'static site', 'web tool', 'website', 'dashboard',
                    'visualiz', 'chart', 'graph', 'svg', 'pdf']
    output_poor = ['mobile app', 'ios app', 'android app', 'mobile client',
                   'browser extension', 'chrome extension',
                   'infrastructure', 'backend only',
                   'library', 'framework', 'sdk', 'plugin',
                   'ios', 'android']
    
    if not (is_non_buildable or is_news_category):
        if any(kw in text for kw in output_great):
            output_score = 2
            output_reason = "CLI/web/visual output, immediately demonstrable"
        elif any(kw in text for kw in output_poor):
            output_score = 0
            output_reason = "Mobile/extension/library, hard to demonstrate"
    
    breakdown = {
        'api': api_score,
        'scope': scope_score,
        'time': time_score,
        'differentiation': diff_score,
        'output': output_score,
    }
    
    total = sum(breakdown.values())
    
    reasoning = (
        f"API({api_score}): {api_reason}. "
        f"Scope({scope_score}): {scope_reason}. "
        f"Time({time_score}): {time_reason}. "
        f"Diff({diff_score}): {diff_reason}. "
        f"Output({output_score}): {output_reason}."
    )
    
    return total, breakdown, reasoning


# ============================================================================
# Cross-Source Amplification
# ============================================================================

def get_amplification_factor(source_count: int) -> float:
    """Get amplification multiplier based on number of sources."""
    if source_count <= 1:
        return 1.0
    elif source_count == 2:
        return 1.3
    elif source_count == 3:
        return 1.5
    else:
        return 2.0


# ============================================================================
# Final Score Calculation
# ============================================================================

def calculate_final_score(
    engagement_normalized: float,
    buildability_score: int,
    amplification_factor: float,
    auto_modifier: int,
) -> float:
    """
    Calculate final composite score for ranking.
    
    Formula: (engagement_normalized * 0.3 + buildability_adjusted * 7) * amplification_factor
    
    This weights buildability heavily (it's the primary signal for The Foundry)
    while still considering engagement (market validation).
    """
    buildability_adjusted = max(0, min(10, buildability_score + auto_modifier))
    # Composite: buildability is primary (70%), engagement is secondary (30%)
    composite = (engagement_normalized * 0.3) + (buildability_adjusted * 7.0)
    return round(composite * amplification_factor, 2)


# ============================================================================
# Main Processing Pipeline
# ============================================================================

def process_trends(input_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Main processing pipeline for Epic 1.2.
    
    Args:
        input_path: Path to trends-raw.json
        output_dir: Directory for output files
        
    Returns:
        Processing statistics
    """
    # Load raw trends
    with open(input_path, 'r') as f:
        raw_data = json.load(f)
    
    trends = raw_data['trends']
    scan_date = raw_data.get('scan_date', datetime.now().isoformat())
    
    print(f"📥 Loaded {len(trends)} raw trends")
    
    # Step 1: Deduplicate across sources
    deduped = deduplicate_trends(trends)
    duplicates_merged = len(trends) - len(deduped)
    print(f"🔗 Deduplication: {len(trends)} → {len(deduped)} ({duplicates_merged} duplicates merged)")
    
    # Step 2: Auto-filter
    filtered = []
    rejected = []
    for trend in deduped:
        filters = check_auto_filters(trend)
        if filters:
            rejected.append({
                'title': trend.get('raw_title', trend.get('title', '')),
                'source': trend.get('source', ''),
                'filters_triggered': filters,
            })
        else:
            trend['auto_filters_triggered'] = []
            filtered.append(trend)
    
    print(f"🚫 Auto-filters: {len(rejected)} trends rejected, {len(filtered)} remaining")
    for r in rejected:
        print(f"   ❌ [{r['source']}] {r['title'][:60]}... → {r['filters_triggered']}")
    
    # Step 3: Normalize engagement, score buildability, apply modifiers
    scored_trends = []
    for trend in filtered:
        # Normalize engagement
        eng_normalized = normalize_engagement(
            trend['engagement_value'],
            trend['source']
        )
        
        # Buildability scoring
        build_score, build_breakdown, build_reasoning = score_buildability(trend)
        
        # Auto-modifiers
        auto_mod, mod_reasons = calculate_auto_modifiers(trend)
        
        # Amplification
        source_count = trend.get('source_count', 1)
        amp_factor = get_amplification_factor(source_count)
        
        # Final score
        final_score = calculate_final_score(
            eng_normalized, build_score, amp_factor, auto_mod
        )
        
        # Attach scores to trend
        trend['engagement_normalized'] = round(eng_normalized, 1)
        trend['buildability_score'] = build_score
        trend['buildability_adjusted'] = max(0, min(10, build_score + auto_mod))
        trend['buildability_breakdown'] = build_breakdown
        trend['buildability_reasoning'] = build_reasoning
        trend['auto_modifiers_applied'] = mod_reasons
        trend['amplification_factor'] = amp_factor
        trend['final_score'] = final_score
        
        scored_trends.append(trend)
    
    # Step 4: Sort by final score (descending)
    scored_trends.sort(key=lambda t: t['final_score'], reverse=True)
    
    # Step 5: Assign new IDs
    date_str = scan_date[:10].replace('-', '')
    for idx, trend in enumerate(scored_trends):
        trend['id'] = f"trend-{date_str}-{idx+1:03d}"
    
    # Step 6: Generate two-tier output
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Top 15 for summary
    top_15 = scored_trends[:15]
    
    # Summary schema (compact, for Spec Writer)
    summary = {
        "schema_version": 1,
        "scan_date": scan_date,
        "processing_date": datetime.now().isoformat(),
        "raw_trends_count": len(trends),
        "after_dedup_count": len(deduped),
        "after_filter_count": len(filtered),
        "trends_count": len(top_15),
        "auto_filters_rejected": len(rejected),
        "duplicates_merged": duplicates_merged,
        "trends": [
            {
                "id": t['id'],
                "title": t.get('raw_title', t.get('title', '')),
                "source": t['source'],
                "sources": list(set(s['source'] for s in t.get('all_sources', [{'source': t['source']}]))),
                "engagement_normalized": t['engagement_normalized'],
                "amplification_factor": t['amplification_factor'],
                "buildability_score": t['buildability_adjusted'],
                "buildability_breakdown": t['buildability_breakdown'],
                "final_score": t['final_score'],
                "summary": t.get('summary', ''),
                "url": t.get('source_url', ''),
            }
            for t in top_15
        ]
    }
    
    summary_path = output_path / 'trends-summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"📋 Summary written: {summary_path} ({len(top_15)} trends)")
    
    # Full detail schema (verbose, for debugging)
    full_dir = output_path / 'trends-full'
    full_dir.mkdir(parents=True, exist_ok=True)
    
    for trend in scored_trends:
        # Build engagement_raw from all sources
        engagement_raw = {}
        for src in trend.get('all_sources', [{'source': trend['source'], 'engagement_value': trend['engagement_value']}]):
            key = f"{src['source']}_{src.get('engagement_metric', 'score')}"
            engagement_raw[key] = src['engagement_value']
        
        full_detail = {
            "schema_version": 1,
            "id": trend['id'],
            "title": trend.get('raw_title', trend.get('title', '')),
            "sources": list(set(s['source'] for s in trend.get('all_sources', [{'source': trend['source']}]))),
            "source_urls": [s.get('source_url', '') for s in trend.get('all_sources', [{'source_url': trend.get('source_url', '')}])],
            "engagement_raw": engagement_raw,
            "engagement_normalized": trend['engagement_normalized'],
            "amplification_factor": trend['amplification_factor'],
            "buildability_score": trend['buildability_adjusted'],
            "buildability_breakdown": trend['buildability_breakdown'],
            "buildability_reasoning": trend['buildability_reasoning'],
            "auto_filters_triggered": trend.get('auto_filters_triggered', []),
            "auto_modifiers_applied": trend.get('auto_modifiers_applied', []),
            "final_score": trend['final_score'],
            "category": trend.get('category', ''),
            "comment_count": trend.get('comment_count', 0),
            "summary": trend.get('summary', ''),
            "raw_data": trend.get('raw_data', {}),
        }
        
        detail_path = full_dir / f"{trend['id']}.json"
        with open(detail_path, 'w') as f:
            json.dump(full_detail, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Full details written: {full_dir}/ ({len(scored_trends)} files)")
    
    # Print top trends
    print(f"\n🏆 Top 15 Trends (by final score):")
    print(f"{'Rank':<5} {'Score':<8} {'Build':<6} {'Eng':<6} {'Amp':<5} {'Source':<8} {'Title'}")
    print("-" * 100)
    for idx, t in enumerate(top_15):
        sources = list(set(s['source'] for s in t.get('all_sources', [{'source': t['source']}])))
        source_str = '+'.join(sources)
        title = t.get('raw_title', t.get('title', ''))[:55]
        print(f"{idx+1:<5} {t['final_score']:<8} {t['buildability_adjusted']:<6} {t['engagement_normalized']:<6} {t['amplification_factor']:<5} {source_str:<8} {title}")
    
    # Stats
    stats = {
        'raw_count': len(trends),
        'after_dedup': len(deduped),
        'duplicates_merged': duplicates_merged,
        'auto_filtered': len(rejected),
        'after_filter': len(filtered),
        'top_15_count': len(top_15),
        'total_scored': len(scored_trends),
        'rejected_trends': rejected,
        'top_3': [
            {
                'title': t.get('raw_title', t.get('title', '')),
                'final_score': t['final_score'],
                'buildability': t['buildability_adjusted'],
                'sources': list(set(s['source'] for s in t.get('all_sources', [{'source': t['source']}]))),
            }
            for t in top_15[:3]
        ],
    }
    
    return stats


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    # Default paths
    input_path = Path.home() / '.openclaw/workspace/foundry/2026-02-18/trends-raw.json'
    output_dir = Path.home() / '.openclaw/workspace/foundry/2026-02-18'
    
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    
    print(f"🏭 Epic 1.2: Trend Scout - Normalization & Scoring")
    print(f"📂 Input: {input_path}")
    print(f"📂 Output: {output_dir}")
    print()
    
    stats = process_trends(str(input_path), str(output_dir))
    
    print(f"\n✅ Processing complete!")
    print(f"   Raw: {stats['raw_count']} → Deduped: {stats['after_dedup']} → Filtered: {stats['after_filter']}")
    print(f"   Duplicates merged: {stats['duplicates_merged']}")
    print(f"   Auto-filtered: {stats['auto_filtered']}")
    print(f"\n🏆 Top 3:")
    for i, t in enumerate(stats['top_3']):
        print(f"   {i+1}. {t['title'][:70]} (score: {t['final_score']}, build: {t['buildability']}, src: {'+'.join(t['sources'])})")
