# Natural Language to SQL Using AI

A natural language to SQL query converter powered by OpenAI and LangChain. This application allows users to interact with a database using natural language queries, which are then converted into SQL and executed against a PostgreSQL database.

## Features

- Interactive REPL (Read-Eval-Print Loop) for natural language database queries
- Translates natural language questions into SQL queries
- Executes queries against a PostgreSQL database
- Docker-based setup for easy deployment
- Sample e-commerce database included

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for running PostgreSQL)
- OpenAI API key

## Installation

1. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecommerce
OPENAI_API_KEY=your_openai_api_key
OPENAI_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

## Database Setup

The project includes a Docker Compose configuration to run PostgreSQL with sample e-commerce data.

1. Start the PostgreSQL container:
```bash
docker compose up -d
```

This will:
- Start a PostgreSQL 14 database
- Create an 'ecommerce' database
- Load the sample e-commerce schema and data
- Expose the database on port 5432

## Usage

Run the application:
```bash
python main.py
```

Once the application starts, you can enter natural language queries at the prompt:

```
AI Database Agent — type 'exit' to quit
Query> Show me all products that cost more than $500
```

Example queries:
- "List all users"
- "Show me the most expensive product"
- "How many orders does each user have?"
- "What's the total value of all orders?"
- "Show products with low stock (less than 15 items)"

Type 'exit' or 'quit' to exit the application.

## Sample Database Schema

The included e-commerce database contains the following tables:
- `users`: Customer information
- `products`: Product catalog with prices and stock levels
- `orders`: Order information with status
- `order_items`: Items within orders

## How It Works

1. The application connects to the PostgreSQL database
2. It creates an AI agent using OpenAI's language models via LangChain
3. User queries in natural language are processed by the agent
4. The agent generates appropriate SQL queries
5. SQL queries are executed against the database
6. Results are presented to the user

## License

[MIT](LICENSE)