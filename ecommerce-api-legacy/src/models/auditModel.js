const { db } = require('../database');

const AuditModel = {
    log: (action) =>
        db.run("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]),
};

module.exports = AuditModel;
