# Vexy Markliff Integration Guide

This guide provides comprehensive examples for integrating vexy-markliff into various applications and workflows.

## Table of Contents

- [Basic Integration Patterns](#basic-integration-patterns)
- [Web Framework Integration](#web-framework-integration)
- [Batch Processing](#batch-processing)
- [Translation Workflow Integration](#translation-workflow-integration)
- [Custom Processing Pipelines](#custom-processing-pipelines)
- [Performance Optimization](#performance-optimization)
- [Error Handling Strategies](#error-handling-strategies)

## Basic Integration Patterns

### Simple Library Usage

```python
from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig
from vexy_markliff.exceptions import VexyMarkliffError

def convert_markdown_file(input_file: str, output_file: str, source_lang: str = "en", target_lang: str = "es"):
    """Convert a Markdown file to XLIFF format."""
    try:
        # Initialize converter with configuration
        config = ConversionConfig(
            split_sentences=True,
            preserve_whitespace=True,
            max_file_size_mb=50
        )
        converter = VexyMarkliff(config)

        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert to XLIFF
        xliff_content = converter.markdown_to_xliff(
            markdown_content, source_lang, target_lang
        )

        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xliff_content)

        return True

    except VexyMarkliffError as e:
        print(f"Conversion failed: {e}")
        return False
```

### Configuration-Driven Processing

```python
from pathlib import Path
from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig, load_config_with_env_override

class DocumentProcessor:
    def __init__(self, config_path: Path = None):
        """Initialize processor with optional configuration file."""
        if config_path:
            self.config = ConversionConfig.from_file(config_path)
        else:
            # Load configuration with environment variable overrides
            self.config = load_config_with_env_override()

        self.converter = VexyMarkliff(self.config)

    def process_document(self, input_path: Path, output_path: Path = None) -> Path:
        """Process a single document with automatic output path generation."""
        if output_path is None:
            output_path = input_path.with_suffix('.xlf')

        # Determine file type and process accordingly
        if input_path.suffix.lower() == '.md':
            return self._process_markdown(input_path, output_path)
        elif input_path.suffix.lower() in ['.html', '.htm']:
            return self._process_html(input_path, output_path)
        else:
            raise ValueError(f"Unsupported file type: {input_path.suffix}")

    def _process_markdown(self, input_path: Path, output_path: Path) -> Path:
        """Process Markdown file."""
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        xliff = self.converter.markdown_to_xliff(
            content,
            self.config.source_language,
            self.config.target_language
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xliff)

        return output_path

    def _process_html(self, input_path: Path, output_path: Path) -> Path:
        """Process HTML file."""
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        xliff = self.converter.html_to_xliff(
            content,
            self.config.source_language,
            self.config.target_language
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xliff)

        return output_path

# Usage
processor = DocumentProcessor(Path("config.yaml"))
output_file = processor.process_document(Path("document.md"))
```

## Web Framework Integration

### Flask Application

```python
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
import os
from pathlib import Path

from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig
from vexy_markliff.exceptions import VexyMarkliffError

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize converter
config = ConversionConfig(max_file_size_mb=50)
converter = VexyMarkliff(config)

@app.route('/convert/text', methods=['POST'])
def convert_text():
    """Convert text content to XLIFF."""
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'error': 'Missing content'}), 400

        content = data['content']
        content_type = data.get('type', 'markdown')  # markdown or html
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'es')

        # Convert based on content type
        if content_type == 'markdown':
            xliff = converter.markdown_to_xliff(content, source_lang, target_lang)
        elif content_type == 'html':
            xliff = converter.html_to_xliff(content, source_lang, target_lang)
        else:
            return jsonify({'error': 'Unsupported content type'}), 400

        return jsonify({
            'xliff': xliff,
            'source_lang': source_lang,
            'target_lang': target_lang
        })

    except VexyMarkliffError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/convert/file', methods=['POST'])
def convert_file():
    """Convert uploaded file to XLIFF."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Security: validate file extension
        filename = secure_filename(file.filename)
        if not filename.lower().endswith(('.md', '.html', '.htm')):
            return jsonify({'error': 'Unsupported file type'}), 400

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode='w+', suffix=Path(filename).suffix, delete=False) as temp_file:
            content = file.read().decode('utf-8')
            temp_file.write(content)
            temp_input_path = temp_file.name

        try:
            # Process the file
            source_lang = request.form.get('source_lang', 'en')
            target_lang = request.form.get('target_lang', 'es')

            if filename.lower().endswith('.md'):
                xliff = converter.markdown_to_xliff(content, source_lang, target_lang)
            else:  # HTML file
                xliff = converter.html_to_xliff(content, source_lang, target_lang)

            # Create output file
            output_filename = Path(filename).with_suffix('.xlf').name
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xlf', delete=False) as output_file:
                output_file.write(xliff)
                output_path = output_file.name

            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/xml'
            )

        finally:
            # Clean up temporary input file
            os.unlink(temp_input_path)

    except VexyMarkliffError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'vexy-markliff'})

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Application

```python
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import tempfile
import io
from pathlib import Path

from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig
from vexy_markliff.exceptions import VexyMarkliffError

app = FastAPI(title="Vexy Markliff API", version="1.0.0")

# Initialize converter
config = ConversionConfig(max_file_size_mb=50)
converter = VexyMarkliff(config)

class ConversionRequest(BaseModel):
    content: str = Field(..., description="Content to convert")
    content_type: Literal["markdown", "html"] = Field(default="markdown", description="Type of content")
    source_lang: str = Field(default="en", description="Source language code")
    target_lang: str = Field(default="es", description="Target language code")

class ConversionResponse(BaseModel):
    xliff: str = Field(..., description="Generated XLIFF content")
    source_lang: str = Field(..., description="Source language")
    target_lang: str = Field(..., description="Target language")
    statistics: dict = Field(..., description="Conversion statistics")

@app.post("/convert/text", response_model=ConversionResponse)
async def convert_text(request: ConversionRequest):
    """Convert text content to XLIFF format."""
    try:
        # Convert based on content type
        if request.content_type == "markdown":
            xliff = converter.markdown_to_xliff(
                request.content, request.source_lang, request.target_lang
            )
        elif request.content_type == "html":
            xliff = converter.html_to_xliff(
                request.content, request.source_lang, request.target_lang
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported content type")

        # Calculate statistics
        stats = {
            "original_length": len(request.content),
            "xliff_length": len(xliff),
            "source_words": len(request.content.split()),
            "content_type": request.content_type
        }

        return ConversionResponse(
            xliff=xliff,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            statistics=stats
        )

    except VexyMarkliffError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/convert/file")
async def convert_file(
    file: UploadFile = File(...),
    source_lang: str = Form(default="en"),
    target_lang: str = Form(default="es")
):
    """Convert uploaded file to XLIFF format."""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.md', '.html', '.htm')):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')

        # Determine file type and convert
        if file.filename.lower().endswith('.md'):
            xliff = converter.markdown_to_xliff(content_str, source_lang, target_lang)
        else:  # HTML file
            xliff = converter.html_to_xliff(content_str, source_lang, target_lang)

        # Create response stream
        xliff_bytes = xliff.encode('utf-8')
        xliff_stream = io.BytesIO(xliff_bytes)

        # Generate output filename
        output_filename = Path(file.filename).with_suffix('.xlf').name

        return StreamingResponse(
            io.BytesIO(xliff_bytes),
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )

    except VexyMarkliffError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "vexy-markliff"}

# Add middleware for CORS if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Batch Processing

### Parallel File Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from typing import List, Tuple
import logging

from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig
from vexy_markliff.exceptions import VexyMarkliffError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self, config_path: Path = None, max_workers: int = 4):
        """Initialize batch processor."""
        self.config = ConversionConfig.from_file(config_path) if config_path else ConversionConfig()
        self.max_workers = max_workers

    def process_single_file(self, input_path: Path, output_dir: Path) -> Tuple[Path, bool, str]:
        """Process a single file and return result."""
        try:
            converter = VexyMarkliff(self.config)

            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert based on file extension
            if input_path.suffix.lower() == '.md':
                xliff = converter.markdown_to_xliff(
                    content,
                    self.config.source_language,
                    self.config.target_language
                )
            elif input_path.suffix.lower() in ['.html', '.htm']:
                xliff = converter.html_to_xliff(
                    content,
                    self.config.source_language,
                    self.config.target_language
                )
            else:
                return input_path, False, f"Unsupported file type: {input_path.suffix}"

            # Write output file
            output_path = output_dir / f"{input_path.stem}.xlf"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xliff)

            return input_path, True, str(output_path)

        except Exception as e:
            return input_path, False, str(e)

    async def process_files_async(self, input_dir: Path, output_dir: Path,
                                  file_pattern: str = "*.md") -> List[Tuple[Path, bool, str]]:
        """Process multiple files asynchronously."""
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find input files
        input_files = list(input_dir.glob(file_pattern))
        if not input_files:
            logger.warning(f"No files found matching pattern: {file_pattern}")
            return []

        logger.info(f"Processing {len(input_files)} files...")

        # Process files in parallel using thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = [
                loop.run_in_executor(
                    executor,
                    self.process_single_file,
                    input_file,
                    output_dir
                )
                for input_file in input_files
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append((input_files[i], False, str(result)))
            else:
                processed_results.append(result)

        # Log summary
        successful = sum(1 for _, success, _ in processed_results if success)
        failed = len(processed_results) - successful
        logger.info(f"Processing complete: {successful} successful, {failed} failed")

        return processed_results

    def process_files_sync(self, input_dir: Path, output_dir: Path,
                          file_pattern: str = "*.md") -> List[Tuple[Path, bool, str]]:
        """Process multiple files synchronously."""
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find input files
        input_files = list(input_dir.glob(file_pattern))
        if not input_files:
            logger.warning(f"No files found matching pattern: {file_pattern}")
            return []

        logger.info(f"Processing {len(input_files)} files...")

        results = []
        for input_file in input_files:
            result = self.process_single_file(input_file, output_dir)
            results.append(result)

            # Log progress
            if len(results) % 10 == 0:
                logger.info(f"Processed {len(results)}/{len(input_files)} files")

        # Log summary
        successful = sum(1 for _, success, _ in results if success)
        failed = len(results) - successful
        logger.info(f"Processing complete: {successful} successful, {failed} failed")

        return results

# Usage examples
async def main():
    # Initialize processor
    processor = BatchProcessor(
        config_path=Path("batch-config.yaml"),
        max_workers=8
    )

    # Process all Markdown files in a directory
    results = await processor.process_files_async(
        input_dir=Path("input_documents"),
        output_dir=Path("output_xliff"),
        file_pattern="*.md"
    )

    # Print results
    for input_path, success, result in results:
        if success:
            print(f"✓ {input_path.name} -> {Path(result).name}")
        else:
            print(f"✗ {input_path.name}: {result}")

# Run the batch processor
if __name__ == "__main__":
    asyncio.run(main())
```

### Directory Watching and Auto-Processing

```python
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig

class DocumentWatcher(FileSystemEventHandler):
    def __init__(self, input_dir: Path, output_dir: Path, config_path: Path = None):
        """Initialize document watcher."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load configuration
        self.config = ConversionConfig.from_file(config_path) if config_path else ConversionConfig()
        self.converter = VexyMarkliff(self.config)

        print(f"Watching {self.input_dir} for changes...")
        print(f"Output directory: {self.output_dir}")

    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            self.process_file(Path(event.src_path))

    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory:
            self.process_file(Path(event.src_path))

    def process_file(self, file_path: Path):
        """Process a single file."""
        try:
            # Only process supported file types
            if file_path.suffix.lower() not in ['.md', '.html', '.htm']:
                return

            print(f"Processing: {file_path.name}")

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert based on file type
            if file_path.suffix.lower() == '.md':
                xliff = self.converter.markdown_to_xliff(
                    content,
                    self.config.source_language,
                    self.config.target_language
                )
            else:  # HTML file
                xliff = self.converter.html_to_xliff(
                    content,
                    self.config.source_language,
                    self.config.target_language
                )

            # Write output file
            output_path = self.output_dir / f"{file_path.stem}.xlf"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xliff)

            print(f"✓ Generated: {output_path.name}")

        except Exception as e:
            print(f"✗ Failed to process {file_path.name}: {e}")

def start_watching(input_dir: str, output_dir: str, config_path: str = None):
    """Start watching directory for changes."""
    event_handler = DocumentWatcher(
        input_dir=Path(input_dir),
        output_dir=Path(output_dir),
        config_path=Path(config_path) if config_path else None
    )

    observer = Observer()
    observer.schedule(event_handler, str(input_dir), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()

    observer.join()

# Usage
if __name__ == "__main__":
    start_watching(
        input_dir="watched_documents",
        output_dir="auto_generated_xliff",
        config_path="watcher-config.yaml"
    )
```

## Translation Workflow Integration

### Translation Memory Integration

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
import sqlite3
from pathlib import Path

from vexy_markliff import VexyMarkliff
from vexy_markliff.config import ConversionConfig

@dataclass
class TMMatch:
    source: str
    target: str
    score: float
    context: Optional[str] = None

class TranslationMemory:
    def __init__(self, db_path: Path):
        """Initialize Translation Memory database."""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize TM database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tm_segments (
                    id INTEGER PRIMARY KEY,
                    source_text TEXT NOT NULL,
                    target_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_source_text ON tm_segments(source_text)
            """)

    def add_segment(self, source: str, target: str, source_lang: str, target_lang: str, context: str = None):
        """Add a segment to the translation memory."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO tm_segments (source_text, target_text, source_lang, target_lang, context)
                VALUES (?, ?, ?, ?, ?)
            """, (source, target, source_lang, target_lang, context))

    def query_matches(self, source_text: str, source_lang: str, target_lang: str,
                     min_score: float = 0.7) -> List[TMMatch]:
        """Query translation memory for matches."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT source_text, target_text, context
                FROM tm_segments
                WHERE source_lang = ? AND target_lang = ?
            """, (source_lang, target_lang))

            matches = []
            for row in cursor:
                db_source, db_target, db_context = row
                score = self._calculate_similarity(source_text, db_source)
                if score >= min_score:
                    matches.append(TMMatch(db_source, db_target, score, db_context))

            return sorted(matches, key=lambda m: m.score, reverse=True)

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity score between two texts (simplified)."""
        if text1 == text2:
            return 1.0

        # Simple word-based similarity (you could use more sophisticated algorithms)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

class TMIntegratedProcessor:
    def __init__(self, config: ConversionConfig, tm_db_path: Path):
        """Initialize processor with TM integration."""
        self.converter = VexyMarkliff(config)
        self.config = config
        self.tm = TranslationMemory(tm_db_path)

    def process_with_tm_leverage(self, content: str, content_type: str = "markdown") -> Dict:
        """Process content with TM leverage."""
        # Convert to XLIFF first
        if content_type == "markdown":
            xliff = self.converter.markdown_to_xliff(
                content,
                self.config.source_language,
                self.config.target_language
            )
        else:
            xliff = self.converter.html_to_xliff(
                content,
                self.config.source_language,
                self.config.target_language
            )

        # Extract segments from content (simplified - in reality you'd parse the XLIFF)
        segments = self._extract_segments(content)

        # Find TM matches for each segment
        enriched_segments = []
        tm_statistics = {"exact_matches": 0, "fuzzy_matches": 0, "no_matches": 0}

        for segment in segments:
            matches = self.tm.query_matches(
                segment,
                self.config.source_language,
                self.config.target_language
            )

            segment_data = {
                "source": segment,
                "target": "",
                "tm_matches": matches[:3],  # Top 3 matches
                "match_quality": "no_match"
            }

            if matches:
                best_match = matches[0]
                if best_match.score == 1.0:
                    segment_data["target"] = best_match.target
                    segment_data["match_quality"] = "exact"
                    tm_statistics["exact_matches"] += 1
                elif best_match.score >= 0.8:
                    segment_data["target"] = best_match.target
                    segment_data["match_quality"] = "fuzzy"
                    tm_statistics["fuzzy_matches"] += 1
                else:
                    tm_statistics["no_matches"] += 1
            else:
                tm_statistics["no_matches"] += 1

            enriched_segments.append(segment_data)

        return {
            "xliff": xliff,
            "segments": enriched_segments,
            "tm_statistics": tm_statistics
        }

    def _extract_segments(self, content: str) -> List[str]:
        """Extract segments from content (simplified implementation)."""
        # This is a simplified implementation
        # In practice, you'd want to parse the content more carefully
        import re

        # Split by sentences (basic implementation)
        sentences = re.split(r'[.!?]+', content)
        segments = [s.strip() for s in sentences if s.strip()]

        return segments

    def update_tm_from_xliff(self, xliff_content: str):
        """Update TM from translated XLIFF content."""
        # Parse XLIFF and extract source/target pairs
        # This is a simplified implementation
        segments = self._parse_xliff_segments(xliff_content)

        for source, target in segments:
            if target:  # Only add if target is available
                self.tm.add_segment(
                    source,
                    target,
                    self.config.source_language,
                    self.config.target_language
                )

    def _parse_xliff_segments(self, xliff_content: str) -> List[tuple]:
        """Parse XLIFF content to extract source/target pairs."""
        # Simplified XLIFF parsing (you'd want to use proper XML parsing)
        import re

        segments = []
        # This is a very basic regex-based approach
        # In practice, use proper XML parsing
        source_pattern = r'<source[^>]*>(.*?)</source>'
        target_pattern = r'<target[^>]*>(.*?)</target>'

        sources = re.findall(source_pattern, xliff_content, re.DOTALL)
        targets = re.findall(target_pattern, xliff_content, re.DOTALL)

        # Pair up sources and targets
        for i, source in enumerate(sources):
            target = targets[i] if i < len(targets) else ""
            segments.append((source.strip(), target.strip()))

        return segments

# Usage example
def demo_tm_integration():
    """Demonstrate TM integration."""
    config = ConversionConfig(source_language="en", target_language="es")
    processor = TMIntegratedProcessor(config, Path("translation_memory.db"))

    # Add some sample TM entries
    processor.tm.add_segment("Hello world", "Hola mundo", "en", "es")
    processor.tm.add_segment("Welcome to our application", "Bienvenido a nuestra aplicación", "en", "es")

    # Process content with TM leverage
    content = """
    # Welcome to our application

    Hello world! This is a test document.

    Welcome to our application. It provides many useful features.
    """

    result = processor.process_with_tm_leverage(content, "markdown")

    print("TM Statistics:", result["tm_statistics"])
    for segment in result["segments"]:
        print(f"Source: {segment['source']}")
        print(f"Target: {segment['target']}")
        print(f"Quality: {segment['match_quality']}")
        if segment["tm_matches"]:
            print(f"Best match score: {segment['tm_matches'][0].score:.2f}")
        print("-" * 40)

if __name__ == "__main__":
    demo_tm_integration()
```

This integration guide provides comprehensive examples for using vexy-markliff in various real-world scenarios. Each section includes complete, runnable code examples that demonstrate best practices for different integration patterns.
