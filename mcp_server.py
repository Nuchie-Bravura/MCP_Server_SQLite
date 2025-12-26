from fastmcp import FastMCP
import sqlite3
import os
from typing import List, Dict, Any

# Initialize the FastMCP application
# This creates an MCP (Model Context Protocol) server named "VideoGameServer"
app = FastMCP("VideoGameServer")

# Database connection function
def get_db_connection():
    """
    Establishes a connection to the SQLite database using relative path.
    Sets row_factory to sqlite3.Row to enable dictionary-like access to rows.
    Returns: sqlite3.Connection object
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build relative path to database (adjust '..' levels based on your folder structure)
    # Current structure assumes: seccion_2/mcp_server.py and DatabaseSample/yourSQLiteDB.db
    db_path = os.path.join(script_dir, 'yourSQLiteDB.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


# MCP Tools (exposed functions that can be called by Claude)

@app.tool()
def get_all_tables() -> List[str]: 
    """ 
    Returns a list of all table names in the database.
    Permits easy access to database structure after connection.
    
    :return: List of table names in the database
    :rtype: List[str]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query SQLite's metadata table to get all table names
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return tables


@app.tool()
def describe_table(table_name: str) -> List[Dict[str, Any]]:
    """
    Returns the schema of a given table in the database.
    Shows column names, types, nullable status, default values, and primary keys.
    
    :param table_name: Name of the table to describe
    :type table_name: str
    :return: List of columns with their details (cid, name, type, notnull, dflt_value, pk)
    :rtype: List[Dict[str, Any]]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # PRAGMA table_info returns column information for the specified table
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return columns


@app.tool()
def execute_query(sql: str) -> List[Dict[str, Any]]:
    """
    Executes a read-only SQL SELECT query on the database.
    
    IMPORTANT: Only SELECT queries (read operations) are allowed.
    INSERT, UPDATE, DELETE, DROP, etc. are NOT permitted for security.
    
    Args:
        sql: SQL SELECT query to execute
        
    Returns:
        List of dictionaries with the query results, or error information if invalid
    """
    # Security validation: only allow SELECT queries
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith('SELECT'):
        return [{
            "error": "Only SELECT queries are allowed",
            "type": "SecurityError"
        }]
    
    # Blocked keywords for additional security
    # Prevents destructive or modifying operations
    prohibited_words = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE']
    if any(word in sql_upper for word in prohibited_words):
        return [{
            "error": f"Query not allowed. Prohibited keywords: {', '.join(prohibited_words)}",
            "type": "SecurityError"
        }]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        
        # Get column names from the cursor description
        columns = [description[0] for description in cursor.description]
        
        # Convert results to list of dictionaries
        # Each row becomes a dict with column names as keys
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        
        return results
    
    except sqlite3.Error as e:
        # Return error information if SQL execution fails
        return [{
            "error": str(e),
            "type": "SQLError"
        }]


# Server startup
if __name__ == "__main__":
    # Starts the MCP server using default settings:
    # - STDIO transport (standard input/output for communication)
    # - Port 5000 (default)
    app.run()

