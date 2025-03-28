const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Redirect HTTP to HTTPS
app.use((req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
        return res.redirect(`https://${req.headers.host}${req.url}`);
    }
    next();
});

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'nb.me/public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'nb.me/public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

