import re


def get_var_keyword(decl):
    pass


def get_var_blocks(decl):
    """
    Extract variable blocks from a declaration string.
    
    Args:
        decl: The declaration string
        
    Returns:
        A list of dictionaries, each with 'name' and 'content' keys representing a variable block
    """
    # First, we need to handle comments to avoid matching VAR blocks inside comments
    # We'll create a version of the string with comments removed for pattern matching
    
    # Create a copy of the original string for processing
    processed_decl = decl
    
    # Remove block comments (* ... *) for pattern matching
    # But we'll keep track of their positions to preserve them in the content
    block_comments = []
    
    def replace_block_comment(match):
        block_comments.append((match.start(), match.end(), match.group(0)))
        return " " * len(match.group(0))  # Replace with spaces to preserve string length
    
    processed_decl = re.sub(r'\(\*.*?\*\)', replace_block_comment, processed_decl, flags=re.DOTALL)
    
    # Handle line comments
    # We'll replace lines that start with // with spaces
    processed_decl = re.sub(r'^\s*//.*$', lambda m: " " * len(m.group(0)), processed_decl, flags=re.MULTILINE)
    
    # Define the pattern to match variable blocks
    # This pattern captures the variable block type (VAR, VAR_INPUT, etc.),
    # and everything up to END_VAR
    pattern = r'\s*(VAR(?:_[A-Za-z_]+)?)(.*?)END_VAR'
    
    # Find all matches in the processed declaration string
    matches = list(re.finditer(pattern, processed_decl, re.DOTALL))
    
    # Convert matches to a list of dictionaries
    blocks = []
    for match in matches:
        var_type = match.group(1).strip()  # VAR, VAR_INPUT, etc.
        content = match.group(2)  # Content between VAR and END_VAR
        
        # Check if this match is inside a block comment
        is_in_comment = False
        for start, end, _ in block_comments:
            if start <= match.start() and match.end() <= end:
                is_in_comment = True
                break
        
        if is_in_comment:
            continue  # Skip this match as it's inside a comment
        
        # Get the actual content from the original string
        start_pos = match.start(2)
        end_pos = match.end(2)
        original_content = decl[start_pos:end_pos]
        
        # Create the block dictionary
        block = {
            "name": var_type,
            "content": original_content
        }
        
        blocks.append(block)
    
    # Always return a list of dictionaries
    return blocks


def get_extend(decl):
    """
    Extract the class names that a function block extends from a declaration string.
    
    Args:
        decl: The declaration string
        
    Returns:
        A list of class names that the function block extends
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r'\(\*.*?\*\)', '', decl, flags=re.DOTALL)
    
    # Remove line comments // ...
    decl_no_comments = re.sub(r'//.*?$', '', decl_no_comments, flags=re.MULTILINE)
    
    # Define the pattern to match "Extends" followed by class names
    # This pattern looks for "Extends" followed by one or more class names separated by commas
    # It stops at "IMPLEMENTS" keyword or end of string
    pattern = r'EXTENDS\s+([\w,\s]+?)(?:\s+IMPLEMENTS\s+|$)'
    
    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)
    
    if match:
        # Extract the matched group (the class names)
        extends_str = match.group(1)
        
        # Split by comma and strip whitespace to get individual class names
        extends_list = [name.strip() for name in extends_str.split(',') if name.strip()]
        
        return extends_list
    
    # Return empty list if no "Extends" found
    return []

def get_implements(decl):
    """
    Extract the interface names that a function block implements from a declaration string.
    
    Args:
        decl: The declaration string
        
    Returns:
        A list of interface names that the function block implements
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r'\(\*.*?\*\)', '', decl, flags=re.DOTALL)
    
    # Remove line comments // ...
    decl_no_comments = re.sub(r'//.*?$', '', decl_no_comments, flags=re.MULTILINE)
    
    # Define the pattern to match "Implements" followed by interface names
    # This pattern looks for "Implements" followed by one or more interface names separated by commas
    # It stops at "EXTENDS" keyword or end of string
    pattern = r'IMPLEMENTS\s+([\w,\s]+?)(?:\s+EXTENDS\s+|$)'
    
    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)
    
    if match:
        # Extract the matched group (the interface names)
        implements_str = match.group(1)
        
        # Split by comma and strip whitespace to get individual interface names
        implements_list = [name.strip() for name in implements_str.split(',') if name.strip()]
        
        return implements_list
    
    # Return empty list if no "Implements" found
    return []

def get_access_modifier(decl):
    """
    Extract the access modifier from a function block declaration string.
    
    Args:
        decl: The declaration string
        
    Returns:
        The access modifier as a string, or an empty string if no access modifier is found
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r'\(\*.*?\*\)', '', decl, flags=re.DOTALL)
    
    # Remove line comments // ...
    decl_no_comments = re.sub(r'//.*?$', '', decl_no_comments, flags=re.MULTILINE)
    
    # Define the pattern to match access modifiers
    # This pattern looks for PRIVATE, PROTECTED, PUBLIC, or INTERNAL keywords
    # It ensures these are standalone words by checking for word boundaries
    pattern = r'\b(PRIVATE|PROTECTED|PUBLIC|INTERNAL)\b'
    
    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)
    
    if match:
        # Return the matched access modifier with its original case
        return match.group(1)
    
    # Return empty string if no access modifier is found
    return ""

def get_abstract_keyword(decl):
    """
    Extract the ABSTRACT keyword from a function block declaration string.
    
    Args:
        decl: The declaration string
        
    Returns:
        The string "ABSTRACT" if the keyword is present, or an empty string if it's not found
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r'\(\*.*?\*\)', '', decl, flags=re.DOTALL)
    
    # Remove line comments // ...
    decl_no_comments = re.sub(r'//.*?$', '', decl_no_comments, flags=re.MULTILINE)
    
    # Define the pattern to match the ABSTRACT keyword
    # This pattern looks for the ABSTRACT keyword as a standalone word
    pattern = r'\b(ABSTRACT)\b'
    
    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)
    
    if match:
        # Return the matched keyword with its original case
        return match.group(1)
    
    # Return empty string if ABSTRACT keyword is not found
    return ""
