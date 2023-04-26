SQL_LITE_DB_FILE=./blurring.db

if [ -f "$SQL_LITE_DB_FILE" ]; then
    echo "there is already an existing DB."
else
    python3 ./db/init_db.py
    echo "blurring DB has been just created."
fi

