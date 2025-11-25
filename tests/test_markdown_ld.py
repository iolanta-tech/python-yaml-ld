from dirty_equals import IsPartialDict

import yaml_ld
from tests.common import tests_root


def test_load_markdown_with_frontmatter():
    """Test loading a Markdown file with YAML front matter."""
    markdown_path = tests_root / 'data' / 'test-markdown-ld.md'

    remote_document = yaml_ld.load_document(markdown_path)

    assert remote_document == IsPartialDict({
        'contentType': 'text/markdown',
        'contextUrl': None,
        'documentUrl': str(markdown_path),
        'document': IsPartialDict({
            '@id': 'https://example.org/person/john-doe',
            '@type': 'Person',
            'name': 'John Doe',
            'description': 'A test person for Markdown-LD testing',
        }),
    })


def test_expand_markdown_ld():
    """Test expanding a Markdown-LD document."""
    markdown_path = tests_root / 'data' / 'test-markdown-ld.md'

    expanded = yaml_ld.expand(markdown_path)

    assert expanded == [
        IsPartialDict({
            '@id': 'https://example.org/person/john-doe',
            '@type': ['https://schema.org/Person'],
        }),
    ]


def test_markdown_ld_without_frontmatter():
    """Test that a Markdown file without front matter returns empty dict."""
    markdown_path = tests_root / 'data' / 'test-markdown-no-frontmatter.md'

    remote_document = yaml_ld.load_document(markdown_path)
    # frontmatter.parse() returns empty dict when no frontmatter is found
    assert remote_document['document'] == {}  # noqa: WPS520


def test_markdown_ld_empty_frontmatter():
    """Test that a Markdown file with empty front matter returns empty dict."""
    markdown_path = tests_root / 'data' / 'test-markdown-empty-frontmatter.md'

    remote_document = yaml_ld.load_document(markdown_path)
    assert remote_document['document'] == {}  # noqa: WPS520
