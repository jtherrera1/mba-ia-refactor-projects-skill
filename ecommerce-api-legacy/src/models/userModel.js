const { db } = require('../database');

const UserModel = {
    findByEmail: (email) =>
        db.get('SELECT * FROM users WHERE email = ?', [email]),

    findById: (id) =>
        db.get('SELECT id, name, email FROM users WHERE id = ?', [id]),

    create: (name, email, hashedPassword) =>
        db.run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [name, email, hashedPassword]),

    deleteById: (id) =>
        db.run('DELETE FROM users WHERE id = ?', [id]),
};

module.exports = UserModel;
