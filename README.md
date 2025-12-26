# MCP Server

MCP (Model Context Protocol) server that provides access to a SQLite video game store database through Claude AI.

## 📋 Prerequisites

Before running this MCP server, make sure you have:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **FastMCP** - MCP server framework

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/videogame-mcp-server.git
cd videogame-mcp-server
```

### 2. Install dependencies

```bash
pip install fastmcp
```

Or if you're using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastmcp
```

## 🎮 Usage

### Running the MCP Server

```bash
python mcp_server.py
```

### Testing with MCP Inspector

To test and debug your server locally:

```bash
fastmcp dev mcp_server.py
```

This will:
- Start a proxy server on `localhost:6277`
- Open a web UI at `localhost:6274`
- Generate an authentication token for secure access

## 🛠️ Available Tools

The server exposes three tools that Claude can use:

### 1. `get_all_tables()`
Returns a list of all table names in the database.

### 2. `describe_table(table_name: str)`
Returns the schema of a specific table (columns, types, constraints).

### 3. `execute_query(sql: str)`
Executes read-only SELECT queries on the database.

**Security:** Only SELECT queries are allowed. INSERT, UPDATE, DELETE, DROP, and other destructive operations are blocked.

## 📁 Project Structure

```
.
├── mcp_server.py           # Main MCP server file
├── yourDB.db               # SQLite database
└── README.md               # This file
```

## 🔒 Security Features

- Read-only access to the database
- SQL injection prevention through query validation
- Blocked destructive operations (DROP, DELETE, UPDATE, etc.)
- Authentication token for MCP Inspector

## 📚 Documentation

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Claude AI Documentation](https://docs.anthropic.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

 JCDiazGomez

- Add FastMCP server implementation with 3 tools
- Add comprehensive README with installation and usage instructions
- Add .gitignore file
- Implement read-only database access with security features"(https://github.com/Nuchie-Bravura/MCP_Server_SQLite)

<img width="1452" height="577" alt="mcp inspector" src="https://github.com/user-attachments/assets/87a782cd-8b6c-432c-a29e-0610764240e2" />


<img width="1222" height="526" alt="Captura de pantalla 2025-12-26 122403" src="https://github.com/user-attachments/assets/7c1b8684-6296-4232-a9ca-fa7e1165288f" />

