const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

router.post('/signup', async (req, res) => {
    const client = req.app.locals.client;
    const db = client.db('repository');
    const usersCollection = db.collection('users');

    const { name, email, password } = req.body;

    try {
        // Check if the email already exists in the database
        const existingUser = await usersCollection.findOne({ email });

        if (existingUser) {
            return res.status(400).json({ message: 'Email already exists' });
        }

        // Insert the new user into the 'users' collection
        await usersCollection.insertOne({ name, email, password });

        // Create a new collection with the user's email as its name
        const userCollection = db.collection(email);

        // Insert a document with initial data into the user's collection
        await userCollection.insertOne({
            cppRating: 0,
            problemSolvingRating: 0,
            easyCount: 0,
            midCount: 0,
            hardCount: 0,
            problems: [] // Initial empty array
        });

        // Send a success response
        res.status(201).json({ message: 'User registered successfully' });
    } catch (error) {
        console.error('Error signing up:', error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});

module.exports = router;
