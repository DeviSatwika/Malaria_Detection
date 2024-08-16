const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 9876;

app.use(cors());

const WINDOW_SIZE = 10;
let numbers = [];

const fetchNumbers = async (type) => {
  try {
    const response = await axios.get(`http://numbersapi.com/${type}`, { timeout: 500 });
    return parseInt(response.data);
  } catch (error) {
    console.error('Error fetching numbers:', error.message);
    return null;
  }
};

app.get('/numbers/:type', async (req, res) => {
  const { type } = req.params;
  
  if (!['p', 'f', 'e', 'r'].includes(type)) {
    return res.status(400).json({ error: 'Invalid number type' });
  }

  const newNumber = await fetchNumbers(type);
  
  if (newNumber !== null) {
    if (!numbers.includes(newNumber)) {
      numbers.push(newNumber);
      if (numbers.length > WINDOW_SIZE) {
        numbers.shift();
      }
    }
  }

  const avg = numbers.length > 0 ? numbers.reduce((sum, num) => sum + num, 0) / numbers.length : 0;

  res.json({
    windowPrevState: numbers.slice(0, -1),
    windowCurrState: numbers,
    numbers: [newNumber],
    avg: parseFloat(avg.toFixed(2))
  });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});