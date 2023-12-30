import re


def parse_markdown(markdown):
    """Removes the frontmatter and html from a markdown string."""
    patterns_without_group = [
        r'---.*---',          # Frontmatter
        r'<figure>.*<\/figure>',  # Figures
        r'<[^>]+>',           # HTML tags
        r'\!\[.*?\]\(.*?\)',  # Images
        r'\# *',               # Headers
        r'\- +',               # Horizontal rules and lists
        r'\> +',               # Blockquotes
        r'\[\^\d\]: ',           # Footnotes
    ]

    text = markdown
    for pattern in patterns_without_group:
        text = re.sub(pattern, '', text, flags=re.DOTALL)

    # Remove common Markdown characters
    patterns = [
        r'\[(.*?)\]\(.*?\)',  # Links
        r'\*\*(.*?)\*\*',     # Bold
        r'\*(.*?)\*',         # Italic
        r'\~\~(.*?)\~\~',     # Strikethrough
        r'\`(.*?)\`',         # Inline code
    ]

    for pattern in patterns:
        text = re.sub(pattern, r'\1', text)

    # Convert multiple spaces to single space
    text = re.sub(r' {2,}', ' ', text)
    # Convert multiple newlines to single newline
    text = re.sub(r'\n{2,}', '\n', text)

    # Strip leading and trailing whitespace
    text = text.strip()
    return text


def chunk_text(text, max_length):
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 <= max_length:  # +1 for the newline
            current_chunk += paragraph + '\n'
        else:
            # remove trailing '\n' from the chunk
            chunks.append(current_chunk.rstrip('\n'))
            current_chunk = paragraph + '\n'

    # add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.rstrip('\n'))

    return chunks
