// loginRoutes.js

const express = require('express');
const router = express.Router();

// POST route to handle login
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    // Access MongoDB client from app locals
    const client = req.app.locals.client;
    const db = client.db('repository'); // Use the 'repository' database

    try {
        // Query the 'users' collection to find the user with the provided email and password
        const user = await db.collection('users').findOne({ email, password });

        if (!user) {
            // If no user is found, return invalid credentials message
            return res.status(400).json({ message: 'Invalid Email or Password' });
        }

        // Delete all documents from the currentUser collection
        await db.collection('currentUser').deleteMany({});

        // Insert the user's email into the 'current_user' collection
        await db.collection('currentUser').insertOne({ email });

        // If email and password are correct, return user information
        return res.status(200).json({ message: 'Login successful', user });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Server Error' });
    }
});

module.exports = router;
