const { getFinancialReport } = require('../services/reportService');

async function financialReport(req, res, next) {
    try {
        const report = await getFinancialReport();
        res.json(report);
    } catch (err) {
        next(err);
    }
}

module.exports = { financialReport };
