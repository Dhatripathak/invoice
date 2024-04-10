// Require necessary modules
const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');
const mongoose = require('mongoose');

// Initialize Express app
const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// MongoDB connection
const uri = 'mongodb://localhost:27017/invoices'; // Define MongoDB URI
const client = new MongoClient(uri); // Create a new MongoClient instance

client.connect((err) => { // Connect to MongoDB server
    if (err) {
        console.error('Error connecting to MongoDB:', err);
        return;
    }
    console.log('Connected to MongoDB server');

    // Access the MongoDB database and collection
    const db = client.db('invoices'); // Access the 'invoices' database
    const shopCollection = db.collection('shopRegistrationDB'); // Access the 'shopRegistrationDB' collection

    // Mongoose connection
    mongoose.connect(uri); // Connect to MongoDB using Mongoose
    const mongooseConnection = mongoose.connection; // Get the default connection

    mongooseConnection.on('error', console.error.bind(console, 'MongoDB connection error:')); // Handle MongoDB connection error
    mongooseConnection.once('open', () => {
        console.log('Connected to MongoDB via Mongoose');
    });

    // Define schema
    const shopSchema = new mongoose.Schema({
        shopName: String,
        shopAddress: String,
        gstNumber: String
    });

    const Shop = mongoose.model('Shop', shopSchema);

    // Routes
    app.post('/register', (req, res) => {
        const newShop = new Shop({
            shopName: req.body.shopName,
            shopAddress: req.body.shopAddress,
            gstNumber: req.body.gstNumber
        });

        newShop.save((err) => {
            if (err) {
                console.error(err);
                res.status(500).send('Error registering the shop');
            } else {
                res.status(200).send('Shop registered successfully');
            }
        });
    });

    // Start server
    const port = 3000;
    app.listen(port, () => {
        console.log(`Server is running on port ${port}`);
    });
});

// Handle connection errors
client.on('error', (err) => {
    console.error('MongoDB connection error:', err);
});

// Handle disconnection events
client.on('disconnected', () => {
    console.log('MongoDB disconnected');
});
