const express = require('express');
const app = express();
const PORT = 3001;

app.get('/', (req, res) => {
  res.send('Hello from Node.js service!');
});

app.listen(PORT, () => {
  console.log(`Node.js service listening on port ${PORT}`);
});
