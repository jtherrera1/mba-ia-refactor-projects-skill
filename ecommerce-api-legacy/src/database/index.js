const sqlite3 = require('sqlite3');
const { hashPassword } = require('../utils/crypto');

class Database {
    constructor() {
        this._db = new sqlite3.Database(':memory:');
    }

    run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this._db.run(sql, params, function (err) {
                if (err) reject(err);
                else resolve({ lastID: this.lastID, changes: this.changes });
            });
        });
    }

    get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this._db.get(sql, params, (err, row) => {
                if (err) reject(err);
                else resolve(row);
            });
        });
    }

    all(sql, params = []) {
        return new Promise((resolve, reject) => {
            this._db.all(sql, params, (err, rows) => {
                if (err) reject(err);
                else resolve(rows);
            });
        });
    }
}

const db = new Database();

async function initDb() {
    await db.run('PRAGMA foreign_keys = ON');
    await db.run(`CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        pass TEXT NOT NULL
    )`);
    await db.run(`CREATE TABLE courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL,
        active INTEGER DEFAULT 1
    )`);
    await db.run(`CREATE TABLE enrollments (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )`);
    await db.run(`CREATE TABLE payments (
        id INTEGER PRIMARY KEY,
        enrollment_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
    )`);
    await db.run(`CREATE TABLE audit_logs (
        id INTEGER PRIMARY KEY,
        action TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    await db.run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
        ['Leonan', 'leonan@fullcycle.com.br', hashPassword('changeme')]);
    await db.run('INSERT INTO courses (title, price, active) VALUES (?, ?, ?)',
        ['Clean Architecture', 997.00, 1]);
    await db.run('INSERT INTO courses (title, price, active) VALUES (?, ?, ?)',
        ['Docker', 497.00, 1]);
    await db.run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [1, 1]);
    await db.run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
        [1, 997.00, 'PAID']);
}

module.exports = { db, initDb };
