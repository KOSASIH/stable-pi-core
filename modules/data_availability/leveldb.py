import leveldb
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LevelDBStorage:
    def __init__(self, db_path: str):
        """Initialize LevelDB storage."""
        self.db = leveldb.LevelDB(db_path)
        logging.info(f"LevelDB initialized at {db_path}")

    def put(self, key: str, value: dict):
        """Store a key-value pair in LevelDB."""
        self.db.Put(key.encode(), json.dumps(value).encode())
        logging.info(f"Stored key: {key}")

    def get(self, key: str) -> dict:
        """Retrieve a value from LevelDB by key."""
        try:
            value = self.db.Get(key.encode())
            logging.info(f"Retrieved key: {key}")
            return json.loads(value.decode())
        except KeyError:
            logging.error(f"Key not found: {key}")
            return None

    def delete(self, key: str):
        """Delete a key-value pair from LevelDB."""
        self.db.Delete(key.encode())
        logging.info(f"Deleted key: {key}")

    def close(self):
        """Close the LevelDB instance."""
        del self.db
        logging.info("LevelDB closed.")

# Example usage
if __name__ == "__main__":
    db = LevelDBStorage("my_leveldb")
    db.put("block_1", {"index": 1, "data": "Sample block data"})
    block_data = db.get("block_1")
    print(f"Retrieved Block Data: {block_data}")
    db.delete("block_1")
    db.close()
