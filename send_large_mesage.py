import discord
import io
import re

LANGUAGE_EXTENSIONS = {
    'python': 'py', 'javascript': 'js', 'java': 'java', 'c': 'c', 'cpp': 'cpp',
    'csharp': 'cs', 'ruby': 'rb', 'php': 'php', 'swift': 'swift', 'go': 'go',
    'rust': 'rs', 'typescript': 'ts', 'kotlin': 'kt', 'scala': 'scala',
    'html': 'html', 'css': 'css', 'sql': 'sql', 'bash': 'sh', 'powershell': 'ps1',
    'markdown': 'md', 'json': 'json', 'xml': 'xml', 'yaml': 'yaml',
    'dockerfile': 'dockerfile', 'tex': 'tex', 'r': 'r', 'matlab': 'm',
    'perl': 'pl', 'lua': 'lua', 'haskell': 'hs', 'julia': 'jl'
}

async def send_large_message(destination, message, replying=True):
    max_length = 2000
    code_block_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
    
    # Extract code blocks
    code_blocks = code_block_pattern.findall(message)
    
    # Remove code blocks from the message
    message_without_code = code_block_pattern.sub('', message)
    
    # Determine the appropriate send method
    async def send(content, file=None):
        if isinstance(destination, discord.TextChannel):
            return await destination.send(content, file=file)
        elif hasattr(destination, 'reply') and replying:
            return await destination.reply(content, file=file)
        else:
            return await destination.send(content, file=file)
    
    # Send the message without code blocks
    if len(message_without_code) <= max_length:
        await send(message_without_code)
    else:
        parts = [message_without_code[i:i+max_length] for i in range(0, len(message_without_code), max_length)]
        await send(parts[0])
        for part in parts[1:]:
            await send(part)
    
    # Send code blocks as files
    for i, (lang, code) in enumerate(code_blocks):
        lang = lang.lower() if lang else 'txt'
        extension = LANGUAGE_EXTENSIONS.get(lang, 'txt')
        file_content = code.strip()
        file = io.StringIO(file_content)
        discord_file = discord.File(file, filename=f"code_block_{i+1}.{extension}")
        await send(f"Code block {i+1} ({lang}):", file=discord_file)
