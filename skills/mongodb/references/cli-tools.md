# MongoDB CLI Reference

**Verified against upstream:** 2026-08-07
**Primary Source:** [MongoDB Database Tools Documentation](https://www.mongodb.com/docs/database-tools/)

This section serves as a comprehensive, production-focused CLI reference for MongoDB operations. It is designed specifically for tech support engineers, database administrators, and DevOps professionals who need to manage, troubleshoot, and recover MongoDB deployments under pressure.

## 1. The MongoDB Shell (`mongosh`)

The MongoDB Shell (`mongosh`) is a fully functional JavaScript and Node.js environment for interacting with MongoDB deployments.

**Connection and Authentication:**
```bash
mongosh "mongodb://localhost:27017"
mongosh "mongodb://db.example.com:27017" --tls --tlsCAFile /etc/ssl/ca.pem --tlsCertificateKeyFile /etc/ssl/client.pem
```

**Advanced Querying and Aggregation:**
```javascript
db.users.find({ status: "active" }, { email: 1, lastLogin: 1, _id: 0 }).sort({ lastLogin: -1 }).limit(100)
```

**Index Management and Optimization:**
```javascript
db.orders.find({ customerId: "CUST-123", status: "shipped" }).explain("executionStats")
db.orders.createIndex({ customerId: 1, status: 1 }, { background: true })
```

**Replica Set and Cluster Management:**
```javascript
rs.status()
rs.stepDown(120)
```

## 2. Data Backup with `mongodump`

`mongodump` is a utility for creating binary exports of the contents of a database.

**Full Database Backup:**
```bash
mongodump --uri="mongodb://user:password@localhost:27017/admin" --out=/backups/full_backup_$(date +%F)
```

**Archiving and Compressing on the Fly:**
```bash
mongodump --uri="mongodb://localhost:27017/mydb" --archive=/backups/mydb_$(date +%F).archive.gz --gzip
```

**Oplog Backups for Point-in-Time Recovery:**
```bash
mongodump --uri="mongodb://localhost:27017/admin" --oplog --out=/backups/oplog_backup
```

## 3. Data Restoration with `mongorestore`

`mongorestore` reads the binary files produced by `mongodump` and restores them to a MongoDB instance.

**Restoring a Full Backup:**
```bash
mongorestore --uri="mongodb://localhost:27017/admin" /backups/full_backup_2023-10-25
```

**Point-in-Time Recovery using the Oplog:**
```bash
mongorestore --uri="mongodb://localhost:27017/admin" --oplogReplay --oplogLimit="1698278400" /backups/oplog_backup
```

## 4. Data Export with `mongoexport`

`mongoexport` produces a JSON or CSV export of data stored in a MongoDB instance.

**Exporting a Collection to JSON:**
```bash
mongoexport --uri="mongodb://localhost:27017/mydb" --collection=users --out=users.json
```

**Exporting to CSV with Specific Fields:**
```bash
mongoexport --uri="mongodb://localhost:27017/mydb" --collection=orders --type=csv --fields="_id,customerId,totalAmount,status" --out=orders.csv
```

## 5. Data Import with `mongoimport`

`mongoimport` imports content from an Extended JSON, CSV, or TSV export created by `mongoexport`.

**Importing a JSON File:**
```bash
mongoimport --uri="mongodb://localhost:27017/mydb" --collection=users --file=users.json
```

**Upserting Data:**
```bash
mongoimport --uri="mongodb://localhost:27017/mydb" --collection=inventory --file=inventory_update.json --mode=upsert --upsertFields=sku
```

## 6. Advanced One-Liners for Daily Operations

**Find the top 5 largest collections in a database:**
```bash
mongosh mydb --quiet --eval 'db.getCollectionNames().map(c => ({name: c, size: db[c].stats().size})).sort((a, b) => b.size - a.size).slice(0, 5)'
```

**Kill all queries running longer than 60 seconds:**
```bash
mongosh admin --quiet --eval 'db.currentOp({ "active": true, "secs_running": { "$gt": 60 } }).inprog.forEach(op => db.killOp(op.opid))'
```

**Export all user emails to a text file:**
```bash
mongoexport --uri="mongodb://localhost:27017/mydb" --collection=users --fields=email --type=csv | tail -n +2 > emails.txt
```

**Monitor replication lag in real-time (run in a loop):**
```bash
watch -n 2 'mongosh admin --quiet --eval "rs.printSlaveReplicationInfo()"'
```
