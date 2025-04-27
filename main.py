import os
import logging
import time
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables first
load_dotenv(override=True)

def initialize_llm():
    """Initialize and configure the language model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    
    model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    api_base_url = os.getenv("OPENAI_URL")
    
    return ChatOpenAI(
        model=model_name,
        temperature=0,
        max_tokens=1000,
        openai_api_key=api_key,
        openai_api_base=api_base_url,
    )

def initialize_database():
    """Initialize and connect to the database."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("Please set the DATABASE_URL environment variable.")
    
    logger.info("Connecting to database...")
    try:
        start_time = time.time()
        
        connect_args = {}
        if database_url.startswith('mssql'):
            connect_args = {"timeout": 30}
        
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            connect_args=connect_args
        )
        
        include_tables = os.getenv("INCLUDE_TABLES", "").split(",") if os.getenv("INCLUDE_TABLES") else None
        
        if include_tables and "" in include_tables:
            include_tables.remove("")
            
        db = SQLDatabase.from_uri(
            database_url,
            include_tables=include_tables,
            sample_rows_in_table_info=0,
            max_string_length=100,
            indexes_in_table_info=False,
            view_support=False,
        )
        
        logger.info(f"Database initialized in {time.time() - start_time:.2f} seconds")
        return db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def create_agent(llm, db):
    """Create an SQL database agent."""
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True,
        top_k=5,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return agent_executor

def run_repl(agent):
    """Run a Read-Eval-Print Loop for interactive queries."""
    print("AI Database Agent — type 'exit' to quit")
    while True:
        query = input("Query> ").strip()
        if not query:
            continue
        
        if query.lower() in ("exit", "quit"):
            break
            
        try:
            logger.info(f"Processing query: {query}")
            result = agent.run(query)
            print("Result:\n", result)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except ValueError as e:
            print(f"Input error: {e}")
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            print(f"Error: {e}")

def main():
    """Main function to initialize components and start the REPL."""
    try:
        logger.info("Initializing language model...")
        llm = initialize_llm()
        
        logger.info("Initializing database...")
        db = initialize_database()
        
        logger.info("Creating SQL agent...")
        agent = create_agent(llm, db)
        
        print("Type 'list tables' to see all tables in the database")
        run_repl(agent)
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        print(f"Error initializing application: {e}")

if __name__ == "__main__":
    main()