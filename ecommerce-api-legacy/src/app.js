const express = require('express');
const { initDb } = require('./database');
const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');
const settings = require('./config/settings');

const app = express();
app.use(express.json());
app.use(routes);
app.use(errorHandler);

initDb()
    .then(() => {
        app.listen(settings.port, () => {
            console.log(`LMS API running on port ${settings.port}`);
        });
    })
    .catch((err) => {
        console.error('Failed to initialize database:', err);
        process.exit(1);
    });
