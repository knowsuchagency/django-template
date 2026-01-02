#!/bin/bash

# Only run for PostgreSQL databases
if [[ "$DATABASE_URL" == *"postgresql"* ]]; then
    # Extract schema from search_path in DATABASE_URL
    SCHEMA=$(echo "$DATABASE_URL" | sed -n 's/.*search_path=\([^&"]*\).*/\1/p' | sed 's/%20/ /g')
    
    if [ -n "$SCHEMA" ]; then
        # Extract connection string without options
        DB_CONN=$(echo "$DATABASE_URL" | sed 's/?.*//')
        
        echo "Ensuring schema $SCHEMA exists..."
        psql "$DB_CONN" -c "CREATE SCHEMA IF NOT EXISTS \"$SCHEMA\";" 2>/dev/null || true
        
        # Extract username from DATABASE_URL
        DB_USER=$(echo "$DATABASE_URL" | sed -n 's|.*://\([^:]*\):.*|\1|p')
        
        echo "Granting permissions on schema $SCHEMA to user $DB_USER..."
        psql "$DB_CONN" -c "GRANT ALL ON SCHEMA \"$SCHEMA\" TO $DB_USER;" 2>/dev/null || true
    fi
fi