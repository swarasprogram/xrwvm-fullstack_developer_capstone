// server/database/app.js
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.json());

// Load seed JSON (files live next to app.js)
const reviews_data = JSON.parse(fs.readFileSync('reviews.json', 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync('dealerships.json', 'utf8'));

// Connect to local Mongo (you imported into DB "dealership")
mongoose.connect('mongodb://127.0.0.1:27017/', { dbName: 'dealership' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

// Seed (idempotent-ish because we wipe first)
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data.reviews || reviews_data);
    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data.dealerships || dealerships_data);
    console.log('Seeded Mongo with reviews & dealers');
  } catch (err) {
    console.error('Seeding error:', err.message);
  }
})();

// Home
app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// --- Reviews ---

// All reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const docs = await Reviews.find().lean();
    res.json(docs);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Reviews by dealer (path param)
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    const docs = await Reviews.find({ dealership: dealerId }).lean();
    res.json(docs);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// --- Dealers ---

// All dealers
app.get('/fetchDealers', async (req, res) => {
  try {
    const docs = await Dealerships.find().lean();
    res.json(docs);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

// Dealers by state (path param, case-insensitive match)
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const docs = await Dealerships.find({ state: { $regex: `^${state}$`, $options: 'i' } }).lean();
    res.json(docs);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

// Dealer by id (path param)
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = Number(req.params.id);
    const doc = await Dealerships.findOne({ id }).lean();
    if (!doc) return res.status(404).json({ error: 'Dealer not found' });
    res.json(doc);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Insert review (kept as-is with a tiny guard)
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = JSON.parse(req.body || '{}');
    const latest = await Reviews.find().sort({ id: -1 }).limit(1);
    const new_id = (latest[0]?.id || 0) + 1;

    const review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: Number(data.dealership),
      review: data.review,
      purchase: !!data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const saved = await review.save();
    res.json(saved);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});