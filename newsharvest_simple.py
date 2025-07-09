# NewsHarvest Pro - Simple Command Line Version
# No Flask required - just run and get results!

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import hashlib
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
from collections import Counter

class SimpleNewsHarvester:
    """Simple but powerful news harvester for command line use"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Bias detection keywords
        self.bias_keywords = {
            'political_left': ['progressive', 'liberal', 'democrat', 'climate change', 'social justice'],
            'political_right': ['conservative', 'republican', 'traditional values', 'law and order'],
            'gender_bias': ['spokesman', 'spokeswoman', 'he said', 'she said'],
            'age_bias': ['young', 'old', 'elderly', 'millennial', 'boomer'],
            'geographic_bias': ['urban', 'rural', 'city', 'countryside'],
            'economic_bias': ['wealthy', 'poor', 'working class', 'elite']
        }
        
        print("🗞️ NewsHarvest Pro - Simple Version Initialized")
        print("✅ Ready for professional news data collection")
    
    def get_webpage(self, url):
        """Fetch webpage with error handling"""
        try:
            time.sleep(random.uniform(1, 2))  # Be respectful to servers
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"⚠️  HTTP {response.status_code} for {url}")
                return None
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    
    def find_article_urls(self, homepage_url):
        """Discover article URLs from news homepage"""
        print(f"🔍 Discovering articles on {homepage_url}")
        
        html_content = self.get_webpage(homepage_url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        all_links = soup.find_all('a', href=True)
        
        article_urls = []
        base_domain = urlparse(homepage_url).netloc
        
        for link in all_links:
            href = link['href']
            absolute_url = urljoin(homepage_url, href)
            
            if self.is_article_url(absolute_url, base_domain):
                article_urls.append(absolute_url)
        
        unique_urls = list(set(article_urls))[:40]  # Remove duplicates, limit for performance
        print(f"📊 Found {len(unique_urls)} potential article URLs")
        return unique_urls
    
    def is_article_url(self, url, base_domain):
        """Check if URL pattern indicates a news article"""
        if base_domain not in url:
            return False
        
        # Patterns that typically indicate news articles
        article_patterns = [
            r'/news/', r'/article/', r'/\d{4}/\d{2}/', r'/world/', 
            r'/politics/', r'/technology/', r'/business/', r'/health/',
            r'/science/', r'/environment/', r'/sports/'
        ]
        
        # Patterns to exclude (not articles)
        exclude_patterns = [
            r'/live/', r'/weather/', r'/search', r'#', r'javascript:',
            r'/video/', r'/gallery/', r'/podcast/', r'/newsletter/',
            r'/subscribe/', r'/contact/', r'/about/'
        ]
        
        # Check if URL matches article patterns
        for pattern in article_patterns:
            if re.search(pattern, url):
                # Ensure it doesn't match exclude patterns
                for exclude in exclude_patterns:
                    if re.search(exclude, url):
                        return False
                return True
        return False
    
    def scrape_article(self, url):
        """Extract article content and metadata"""
        html_content = self.get_webpage(url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title using multiple strategies
        title = None
        title_selectors = [
            'h1[data-testid="headline"]',  # BBC specific
            'h1.story-headline',           # Common news pattern
            'h1.article-title',            # Alternative pattern
            'h1',                          # Generic fallback
            '.headline h1',                # Nested headline
            '.article-header h1'           # Article header
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                title = element.get_text(strip=True)
                break
        
        # Extract content using multiple strategies
        content_paragraphs = []
        content_selectors = [
            '[data-component="text-block"] p',  # BBC specific
            'article p',                        # Semantic HTML
            '.story-body p',                    # Common news class
            '.article-content p',               # Alternative
            '.post-content p',                  # Blog style
            '.content p'                        # Generic content
        ]
        
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs and len(paragraphs) >= 3:  # Need substantial content
                content_paragraphs = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                break
        
        # If no specific content found, try all paragraphs as fallback
        if not content_paragraphs:
            all_paragraphs = soup.select('p')
            if len(all_paragraphs) >= 5:
                content_paragraphs = [p.get_text(strip=True) for p in all_paragraphs if p.get_text(strip=True)]
        
        content = ' '.join(content_paragraphs)
        
        # Extract author information
        author = None
        author_selectors = [
            '.byline', '.author', '[data-component="byline"]',
            '.article-author', '[rel="author"]', '.writer',
            '.journalist', '.correspondent'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                author_text = element.get_text(strip=True)
                if author_text and len(author_text) < 100:  # Reasonable author name length
                    author = author_text
                    break
        
        # Extract publish date
        publish_date = None
        date_selectors = [
            'time[datetime]', '[data-testid="timestamp"]',
            '.date', '.published', '.article-date',
            '.publish-date', '.timestamp'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                date_value = element.get('datetime') or element.get_text(strip=True)
                if date_value:
                    publish_date = date_value
                    break
        
        return {
            'title': title,
            'content': content,
            'url': url,
            'author': author,
            'publish_date': publish_date,
            'scraped_at': datetime.now().isoformat(),
            'word_count': len(content.split()) if content else 0
        }
    
    def calculate_quality_score(self, article):
        """Calculate comprehensive quality score (0-1)"""
        score = 0.0
        
        title = article.get('title', '')
        content = article.get('content', '')
        word_count = article.get('word_count', 0)
        
        # Title quality assessment (0-0.25)
        if title and len(title) >= 10 and not title.isupper():
            if len(title) >= 20:
                score += 0.25  # Good length title
            else:
                score += 0.15  # Acceptable title
        
        # Content length assessment (0-0.35)
        if word_count >= 500:
            score += 0.35  # Excellent length
        elif word_count >= 300:
            score += 0.25  # Good length
        elif word_count >= 200:
            score += 0.20  # Acceptable length
        elif word_count >= 100:
            score += 0.15  # Minimum acceptable
        
        # Content structure quality (0-0.20)
        if content:
            # Check for proper sentence structure
            sentence_endings = content.count('.') + content.count('!') + content.count('?')
            if sentence_endings >= 10:
                score += 0.20  # Well-structured content
            elif sentence_endings >= 5:
                score += 0.15  # Adequately structured
            elif sentence_endings >= 3:
                score += 0.10  # Basic structure
        
        # Language quality assessment (0-0.10)
        if content:
            # Check caps ratio (too many caps = poor quality)
            caps_ratio = sum(1 for c in content if c.isupper()) / len(content) if content else 0
            if caps_ratio <= 0.05:  # Less than 5% caps
                score += 0.10
            elif caps_ratio <= 0.10:  # Less than 10% caps
                score += 0.05
        
        # Metadata completeness (0-0.10)
        if article.get('author'):
            score += 0.05  # Has author
        if article.get('publish_date'):
            score += 0.05  # Has publish date
        
        return min(score, 1.0)  # Cap at 1.0
    
    def analyze_bias(self, text):
        """Perform comprehensive bias analysis"""
        text_lower = text.lower()
        word_count = len(text.split())
        
        if word_count == 0:
            return {
                'bias_density': 0,
                'is_balanced': True,
                'bias_scores': {},
                'concerns': []
            }
        
        bias_scores = {}
        total_bias_indicators = 0
        
        # Count bias indicators by category
        for category, keywords in self.bias_keywords.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            bias_scores[category] = count
            total_bias_indicators += count
        
        # Calculate bias density as percentage
        bias_density = (total_bias_indicators / word_count * 100)
        
        # Determine if article is balanced
        is_balanced = bias_density < 2.0  # Less than 2% bias indicators
        
        # Generate specific concerns
        concerns = []
        if bias_density >= 3.0:
            concerns.append(f"High bias density: {bias_density:.1f}%")
        
        # Check for strong political bias
        left_bias = bias_scores.get('political_left', 0)
        right_bias = bias_scores.get('political_right', 0)
        
        if left_bias > 3 and right_bias == 0:
            concerns.append("Strong left-leaning political language")
        elif right_bias > 3 and left_bias == 0:
            concerns.append("Strong right-leaning political language")
        
        # Check for excessive demographic focus
        demographic_bias = (bias_scores.get('gender_bias', 0) + 
                          bias_scores.get('age_bias', 0) + 
                          bias_scores.get('geographic_bias', 0))
        
        if demographic_bias > 5:
            concerns.append("High demographic bias indicators")
        
        return {
            'bias_density': round(bias_density, 2),
            'is_balanced': is_balanced,
            'bias_scores': bias_scores,
            'total_bias_indicators': total_bias_indicators,
            'concerns': concerns
        }
    
    def harvest_news(self, homepage_url, max_articles=10, quality_threshold=0.6):
        """Main harvesting function with progress display"""
        print(f"\n🎯 Starting NewsHarvest Pro Collection")
        print(f"📡 Source: {homepage_url}")
        print(f"🎚️  Target: {max_articles} articles (Quality ≥ {quality_threshold})")
        print("=" * 60)
        
        # Step 1: Discover article URLs
        article_urls = self.find_article_urls(homepage_url)
        
        if not article_urls:
            print("❌ No article URLs found. Try a different news website.")
            return []
        
        # Step 2: Process articles
        print(f"\n📰 Processing up to {min(len(article_urls), max_articles * 2)} articles...")
        
        collected_articles = []
        processed = 0
        seen_hashes = set()
        
        # Determine source name from URL
        domain = urlparse(homepage_url).netloc.lower()
        if 'bbc' in domain:
            source_name = 'BBC'
        elif 'reuters' in domain:
            source_name = 'Reuters'
        elif 'guardian' in domain:
            source_name = 'Guardian'
        elif 'techcrunch' in domain:
            source_name = 'TechCrunch'
        elif 'cnn' in domain:
            source_name = 'CNN'
        elif 'npr' in domain:
            source_name = 'NPR'
        else:
            source_name = domain.replace('www.', '').replace('.com', '').title()
        
        for i, article_url in enumerate(article_urls[:max_articles * 2], 1):
            processed += 1
            print(f"🔄 Processing {processed}: {article_url[:60]}...")
            
            # Scrape article
            article = self.scrape_article(article_url)
            if not article:
                print("   ❌ Failed to extract content")
                continue
            
            # Add source information
            article['source'] = source_name
            
            # Basic validation
            if not article['title'] or len(article['title']) < 10:
                print("   ❌ Title too short or missing")
                continue
            
            if article['word_count'] < 100:
                print(f"   ❌ Content too short ({article['word_count']} words)")
                continue
            
            # Calculate quality score
            quality_score = self.calculate_quality_score(article)
            article['quality_score'] = quality_score
            
            if quality_score < quality_threshold:
                print(f"   ❌ Quality too low ({quality_score:.2f})")
                continue
            
            # Perform bias analysis
            combined_text = f"{article['title']} {article['content']}"
            bias_analysis = self.analyze_bias(combined_text)
            article['bias_analysis'] = bias_analysis
            
            # Check for duplicates
            content_hash = hashlib.md5(f"{article['title']}{article['content'][:500]}".encode()).hexdigest()
            if content_hash in seen_hashes:
                print("   ❌ Duplicate content")
                continue
            
            seen_hashes.add(content_hash)
            article['content_hash'] = content_hash
            
            # Article passed all checks
            collected_articles.append(article)
            print(f"   ✅ ACCEPTED - Quality: {quality_score:.2f}, Bias: {bias_analysis['bias_density']:.1f}%, Words: {article['word_count']}")
            
            # Stop if we have enough articles
            if len(collected_articles) >= max_articles:
                print(f"\n🎯 Target reached: {max_articles} articles collected")
                break
        
        print("\n" + "=" * 60)
        print(f"📊 COLLECTION COMPLETE")
        print(f"✅ Successfully collected: {len(collected_articles)} articles")
        print(f"📈 Processing efficiency: {len(collected_articles)}/{processed} ({len(collected_articles)/processed*100:.1f}%)")
        
        return collected_articles
    
    def generate_summary_report(self, articles):
        """Generate a comprehensive summary of collected articles"""
        if not articles:
            return "No articles collected."
        
        # Calculate aggregate metrics
        total_articles = len(articles)
        avg_quality = sum(a['quality_score'] for a in articles) / total_articles
        avg_bias = sum(a['bias_analysis']['bias_density'] for a in articles) / total_articles
        avg_words = sum(a['word_count'] for a in articles) / total_articles
        balanced_articles = sum(1 for a in articles if a['bias_analysis']['is_balanced'])
        
        # Source distribution
        sources = [a['source'] for a in articles]
        source_counts = Counter(sources)
        
        # Quality distribution
        excellent_quality = sum(1 for a in articles if a['quality_score'] >= 0.8)
        good_quality = sum(1 for a in articles if 0.6 <= a['quality_score'] < 0.8)
        fair_quality = sum(1 for a in articles if a['quality_score'] < 0.6)
        
        print("\n" + "=" * 60)
        print("📈 DATASET QUALITY ANALYSIS")
        print("=" * 60)
        print(f"📊 Total Articles: {total_articles}")
        print(f"⭐ Average Quality Score: {avg_quality:.3f} / 1.0")
        print(f"⚖️  Average Bias Density: {avg_bias:.2f}%")
        print(f"📝 Average Word Count: {avg_words:.0f}")
        print(f"✅ Balanced Articles: {balanced_articles}/{total_articles} ({balanced_articles/total_articles*100:.1f}%)")
        
        print(f"\n📊 Quality Distribution:")
        print(f"   🏆 Excellent (≥0.8): {excellent_quality} articles")
        print(f"   👍 Good (0.6-0.8): {good_quality} articles")
        print(f"   📖 Fair (<0.6): {fair_quality} articles")
        
        print(f"\n📰 Source Distribution:")
        for source, count in source_counts.most_common():
            percentage = (count / total_articles) * 100
            print(f"   • {source}: {count} articles ({percentage:.1f}%)")
        
        # Bias analysis summary
        all_bias_scores = {}
        for category in self.bias_keywords.keys():
            total_score = sum(a['bias_analysis']['bias_scores'].get(category, 0) for a in articles)
            all_bias_scores[category] = total_score
        
        if any(score > 0 for score in all_bias_scores.values()):
            print(f"\n⚖️  Bias Category Analysis:")
            for category, score in all_bias_scores.items():
                if score > 0:
                    category_name = category.replace('_', ' ').title()
                    print(f"   • {category_name}: {score} indicators")
        
        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        if avg_quality >= 0.8:
            quality_grade = "Excellent"
        elif avg_quality >= 0.6:
            quality_grade = "Good"
        else:
            quality_grade = "Fair"
        
        if avg_bias <= 1.5:
            bias_grade = "Low Bias"
        elif avg_bias <= 3.0:
            bias_grade = "Moderate Bias"
        else:
            bias_grade = "High Bias"
        
        print(f"   📊 Quality Grade: {quality_grade}")
        print(f"   ⚖️  Bias Grade: {bias_grade}")
        print(f"   🏆 Dataset Suitable for: {'Research & Analysis' if avg_quality >= 0.6 else 'Basic Analysis'}")
        
        return articles
    
    def clean_text(self, text):
        """Clean text and fix encoding issues"""
        if not text:
            return text
        
        # Common encoding fixes
        encoding_fixes = {
            'â€™': "'",  # Right single quotation mark
            'â€œ': '"',  # Left double quotation mark  
            'â€': '"',   # Right double quotation mark
            'â€"': '—',  # Em dash
            'â€"': '–',  # En dash
            'â€¦': '...',# Horizontal ellipsis
            'Â': '',     # Non-breaking space artifacts
            'â€²': "'",  # Prime symbol
            'â€³': '"',  # Double prime
            'â„¢': '™',  # Trademark
            'Â®': '®',   # Registered trademark
            'Â©': '©',   # Copyright
            'â‚¬': '€',  # Euro sign
            'Â£': '£',   # Pound sign
            'â€š': ',',  # Single low-9 quotation mark
            'â€ž': '"',  # Double low-9 quotation mark
            'â€¹': '<',  # Single left angle quotation mark
            'â€º': '>',  # Single right angle quotation mark
        }
        
        # Apply fixes
        for bad_char, good_char in encoding_fixes.items():
            text = text.replace(bad_char, good_char)
        
        # Remove any remaining problematic characters
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Clean up extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def save_dataset(self, articles, format='json', filename=None):
        """Save dataset to file with proper encoding"""
        if not articles:
            print("❌ No articles to save")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = filename or f'newsharvest_dataset_{timestamp}.json'
            
            # Clean all text data before saving
            cleaned_articles = []
            for article in articles:
                cleaned_article = {}
                for key, value in article.items():
                    if isinstance(value, str):
                        cleaned_article[key] = self.clean_text(value)
                    elif isinstance(value, dict):
                        # Handle nested dictionaries like bias_analysis
                        cleaned_dict = {}
                        for subkey, subvalue in value.items():
                            if isinstance(subvalue, str):
                                cleaned_dict[subkey] = self.clean_text(subvalue)
                            elif isinstance(subvalue, list):
                                # Handle lists of strings
                                cleaned_dict[subkey] = [self.clean_text(item) if isinstance(item, str) else item for item in subvalue]
                            else:
                                cleaned_dict[subkey] = subvalue
                        cleaned_article[key] = cleaned_dict
                    else:
                        cleaned_article[key] = value
                cleaned_articles.append(cleaned_article)
            
            # Save with proper UTF-8 encoding
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(cleaned_articles, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Dataset saved as JSON: {filename}")
            return filename
        
        elif format == 'csv':
            filename = filename or f'newsharvest_dataset_{timestamp}.csv'
            
            # Flatten articles for CSV
            flattened_articles = []
            for article in articles:
                flat_article = {
                    'title': self.clean_text(article.get('title', '')),
                    'content': self.clean_text(article.get('content', '')),
                    'url': article.get('url', ''),
                    'source': article.get('source', ''),
                    'author': self.clean_text(article.get('author', '')),
                    'publish_date': article.get('publish_date', ''),
                    'word_count': article.get('word_count', 0),
                    'quality_score': article.get('quality_score', 0),
                    'bias_density': article.get('bias_analysis', {}).get('bias_density', 0),
                    'is_balanced': article.get('bias_analysis', {}).get('is_balanced', True),
                    'bias_concerns': '; '.join(article.get('bias_analysis', {}).get('concerns', [])),
                    'scraped_at': article.get('scraped_at', '')
                }
                flattened_articles.append(flat_article)
            
            # Save CSV with proper encoding
            df = pd.DataFrame(flattened_articles)
            df.to_csv(filename, index=False, encoding='utf-8')
            
            print(f"💾 Dataset saved as CSV: {filename}")
            return filename
        
        else:
            print(f"❌ Unsupported format: {format}")
            return None

def main():
    """Main function for command line usage"""
    print("🗞️ NewsHarvest Pro - Simple Command Line Version")
    print("=" * 60)
    print("Professional news data collection with quality control and bias analysis")
    print()
    
    # Initialize harvester
    harvester = SimpleNewsHarvester()
    
    # Interactive mode
    while True:
        try:
            print("\n📋 Enter collection parameters:")
            
            # Get URL from user
            url = input("🌐 News website URL (or 'quit' to exit): ").strip()
            if url.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using NewsHarvest Pro!")
                break
            
            if not url.startswith('http'):
                print("❌ Please enter a valid URL starting with http:// or https://")
                continue
            
            # Get number of articles
            try:
                max_articles = int(input("📊 Number of articles to collect (default 10): ") or "10")
                if max_articles <= 0 or max_articles > 50:
                    print("⚠️  Using default: 10 articles (range: 1-50)")
                    max_articles = 10
            except ValueError:
                max_articles = 10
                print("⚠️  Invalid input, using default: 10 articles")
            
            # Get quality threshold
            try:
                quality_threshold = float(input("🎚️  Quality threshold 0.4-0.8 (default 0.6): ") or "0.6")
                if quality_threshold < 0.4 or quality_threshold > 1.0:
                    print("⚠️  Using default: 0.6 (range: 0.4-1.0)")
                    quality_threshold = 0.6
            except ValueError:
                quality_threshold = 0.6
                print("⚠️  Invalid input, using default: 0.6")
            
            # Start harvesting
            articles = harvester.harvest_news(url, max_articles, quality_threshold)
            
            if articles:
                # Generate summary report
                harvester.generate_summary_report(articles)
                
                # Ask about saving
                print("\n💾 Save dataset?")
                save_format = input("Choose format (json/csv/both/skip): ").strip().lower()
                
                if save_format in ['json', 'both']:
                    harvester.save_dataset(articles, 'json')
                
                if save_format in ['csv', 'both']:
                    harvester.save_dataset(articles, 'csv')
                
                if save_format == 'skip':
                    print("⏭️  Dataset not saved")
                
                print(f"\n✅ Collection complete! {len(articles)} articles processed.")
                
            else:
                print("\n❌ No articles collected. Try a different website or lower quality threshold.")
            
            # Ask if user wants to continue
            continue_choice = input("\n🔄 Collect from another website? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("👋 Thanks for using NewsHarvest Pro!")
                break
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Operation cancelled by user")
            print("👋 Thanks for using NewsHarvest Pro!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("🔄 Please try again with a different URL")

# Example usage function
def example_usage():
    """Show example of how to use the harvester programmatically"""
    print("📖 Example Usage:")
    print("-" * 40)
    
    # Initialize
    harvester = SimpleNewsHarvester()
    
    # Collect articles
    articles = harvester.harvest_news("https://www.bbc.com/news", max_articles=5, quality_threshold=0.6)
    
    # Generate report
    if articles:
        harvester.generate_summary_report(articles)
        
        # Save results
        harvester.save_dataset(articles, 'json')
        harvester.save_dataset(articles, 'csv')
        
        print(f"\n✅ Example complete! Collected {len(articles)} articles")
    else:
        print("❌ Example failed - no articles collected")

if __name__ == "__main__":
    import sys
    
    # Check if user wants example or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        example_usage()
    else:
        main()

# Quick test URLs for copy-paste:
"""
Recommended test URLs:
- https://www.bbc.com/news
- https://techcrunch.com  
- https://www.reuters.com
- https://arstechnica.com
- https://www.theguardian.com/us

Usage:
1. python newsharvest_simple.py
2. Enter a news URL
3. Choose number of articles (5-20 recommended)
4. Choose quality threshold (0.6 recommended)
5. Wait for collection to complete
6. Review quality report
7. Save as JSON/CSV
"""